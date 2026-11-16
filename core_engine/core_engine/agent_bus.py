"""Jarvis OS Agent Bus - UNIX Domain Socket Pub/Sub Broker.

Provides a fast, asynchronous, local inter-process communication (IPC)
bus connecting the Jarvis CEO (Gemini Live) with local specialist workers
(Paperclip, Friday, Ultron, etc.).

Features:
- UNIX Domain Socket broker bound to `/tmp/jarvis_agent_bus.sock`
- Topic-based and type-based pub/sub routing with wildcard pattern matching
- Point-to-point direct routing by target agent ID
- Built-in routing and helpers for standard Jarvis message types:
    * `task.assign`
    * `task.progress`
    * `task.complete`
    * `task.failed`
    * `task.cancel`
    * `agent.heartbeat`
- Clean startup and graceful shutdown sequences with socket file cleanup
- Asynchronous client and server APIs with context manager support
- Heartbeat tracking and client presence management
"""

import argparse
import asyncio
from dataclasses import asdict, dataclass, field
from enum import Enum
import fnmatch
import json
import logging
import os
from pathlib import Path
import signal
import time
from typing import Any, Callable, Dict, List, Optional, Set, Union
import uuid

DEFAULT_SOCKET_PATH = os.environ.get(
    "JARVIS_BUS_SOCKET",
    str(Path(__file__).resolve().parents[2] / "run" / "agent_bus.sock"),
)

logger = logging.getLogger("jarvis.agent_bus")


class MessageType(str, Enum):
    """Standard message types routed across the Jarvis Agent Bus."""

    # Task lifecycle types
    TASK_ASSIGN = "task.assign"
    TASK_PROGRESS = "task.progress"
    TASK_COMPLETE = "task.complete"
    TASK_FAILED = "task.failed"
    TASK_CANCEL = "task.cancel"

    # Agent presence & lifecycle
    AGENT_HEARTBEAT = "agent.heartbeat"
    AGENT_ONLINE = "agent.online"
    AGENT_OFFLINE = "agent.offline"

    # Bus management & control
    BUS_REGISTER = "bus.register"
    BUS_SUBSCRIBE = "bus.subscribe"
    BUS_UNSUBSCRIBE = "bus.unsubscribe"
    BUS_PING = "bus.ping"
    BUS_PONG = "bus.pong"
    BUS_ACK = "bus.ack"
    BUS_ERROR = "bus.error"


@dataclass
class AgentMessage:
    """Standard envelope for messages passed across the agent bus."""

    type: str
    source: str = "anonymous"
    target: Optional[str] = None
    topic: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    reply_to: Optional[str] = None

    def __post_init__(self):
        if not self.topic:
            self.topic = self.type

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_bytes(self) -> bytes:
        return (self.to_json() + "\n").encode("utf-8")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        return cls(
            type=str(data.get("type", "")),
            source=str(data.get("source", "anonymous")),
            target=data.get("target"),
            topic=data.get("topic") or data.get("type"),
            payload=data.get("payload") if isinstance(data.get("payload"), dict) else {},
            msg_id=str(data.get("msg_id", data.get("id", uuid.uuid4()))),
            timestamp=float(data.get("timestamp", time.time())),
            reply_to=data.get("reply_to"),
        )

    @classmethod
    def from_json(cls, raw: Union[str, bytes, dict]) -> "AgentMessage":
        if isinstance(raw, dict):
            return cls.from_dict(raw)
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        raw = raw.strip()
        if not raw:
            raise ValueError("Empty message string")
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("JSON payload must be an object")
        return cls.from_dict(parsed)


def topic_matches(pattern: str, topic: str) -> bool:
    """Check if a topic matches a subscription pattern.

    Supports exact matches, full wildcards ('*', '#'), and glob patterns ('task.*').
    """
    if pattern in ("*", "#"):
        return True
    if pattern == topic:
        return True
    return fnmatch.fnmatch(topic, pattern)


@dataclass(eq=False)
class ConnectedClient:
    """Tracks state of a client connected to the AgentBusServer."""

    writer: asyncio.StreamWriter
    reader: asyncio.StreamReader
    client_id: str = "anonymous"
    subscriptions: Set[str] = field(default_factory=set)
    connected_at: float = field(default_factory=time.time)
    last_heartbeat: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    async def send(self, message: AgentMessage) -> bool:
        """Send a message to this client."""
        try:
            if self.writer.is_closing():
                return False
            self.writer.write(message.to_bytes())
            await self.writer.drain()
            return True
        except (ConnectionResetError, BrokenPipeError, asyncio.CancelledError):
            return False
        except Exception as e:
            logger.debug(f"Failed to send to client {self.client_id}: {e}")
            return False


class AgentBusServer:
    """UNIX Domain Socket Broker for Jarvis multi-agent IPC."""

    def __init__(
        self,
        socket_path: str = DEFAULT_SOCKET_PATH,
        socket_permissions: int = 0o666,
    ):
        self.socket_path = socket_path
        self.socket_permissions = socket_permissions
        self._server: Optional[asyncio.Server] = None
        self._clients: Dict[str, ConnectedClient] = {}
        self._all_clients: Set[ConnectedClient] = set()
        self._handlers: Dict[str, List[Callable[[AgentMessage, ConnectedClient], Any]]] = {}
        self._running = False
        self._lock = asyncio.Lock()
        self._heartbeat_checker_task: Optional[asyncio.Task] = None

    @property
    def is_running(self) -> bool:
        return self._running

    def register_handler(
        self,
        msg_type: str,
        handler: Callable[[AgentMessage, ConnectedClient], Any],
    ) -> None:
        """Register a server-side hook/handler for a specific message type or pattern."""
        self._handlers.setdefault(msg_type, []).append(handler)

    def _cleanup_socket_file(self) -> None:
        """Safely remove the socket file if it exists."""
        try:
            p = Path(self.socket_path)
            if p.exists() or p.is_socket():
                p.unlink(missing_ok=True)
                logger.info(f"Cleaned up existing socket file: {self.socket_path}")
        except Exception as e:
            logger.warning(f"Error removing socket file {self.socket_path}: {e}")

    async def start(self) -> None:
        """Start the UNIX domain socket server."""
        if self._running:
            logger.warning("AgentBusServer is already running")
            return

        # Ensure parent directory exists and clean stale socket
        socket_dir = os.path.dirname(os.path.abspath(self.socket_path))
        os.makedirs(socket_dir, exist_ok=True)
        self._cleanup_socket_file()

        logger.info(f"Starting Jarvis Agent Bus on {self.socket_path}...")
        self._server = await asyncio.start_unix_server(
            self._handle_client_connection,
            path=self.socket_path,
        )

        try:
            os.chmod(self.socket_path, self.socket_permissions)
        except Exception as e:
            logger.warning(f"Could not set permissions {oct(self.socket_permissions)} on socket: {e}")

        self._running = True
        self._heartbeat_checker_task = asyncio.create_task(self._monitor_heartbeats())
        logger.info(f"Jarvis Agent Bus listening on {self.socket_path}")

    async def stop(self) -> None:
        """Gracefully shut down the server and all connections."""
        if not self._running:
            return

        logger.info("Stopping Jarvis Agent Bus server...")
        self._running = False

        if self._heartbeat_checker_task:
            self._heartbeat_checker_task.cancel()
            try:
                await self._heartbeat_checker_task
            except asyncio.CancelledError:
                pass
            self._heartbeat_checker_task = None

        # Notify all connected clients of server shutdown
        shutdown_msg = AgentMessage(
            type="bus.shutdown",
            source="bus_server",
            payload={"message": "Server shutting down"},
        )
        for client in list(self._all_clients):
            try:
                await client.send(shutdown_msg)
                client.writer.close()
                await client.writer.wait_closed()
            except Exception:
                pass

        self._clients.clear()
        self._all_clients.clear()

        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

        self._cleanup_socket_file()
        logger.info("Jarvis Agent Bus server stopped successfully")

    async def __aenter__(self) -> "AgentBusServer":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()

    async def _handle_client_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """Handle individual client socket connection stream."""
        client = ConnectedClient(writer=writer, reader=reader)
        async with self._lock:
            self._all_clients.add(client)

        peer = "unix-socket-client"
        logger.debug(f"New client connection established ({peer})")

        try:
            while self._running:
                line = await reader.readline()
                if not line:
                    break  # Client disconnected

                try:
                    message = AgentMessage.from_json(line)
                except Exception as err:
                    logger.warning(f"Failed to parse incoming message: {err} | Raw: {line!r}")
                    err_msg = AgentMessage(
                        type=MessageType.BUS_ERROR.value,
                        source="bus_server",
                        payload={"error": f"Invalid JSON message format: {err}"},
                    )
                    await client.send(err_msg)
                    continue

                await self._process_message(client, message)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.debug(f"Connection error with client {client.client_id}: {e}")
        finally:
            await self._remove_client(client)

    async def _process_message(self, client: ConnectedClient, message: AgentMessage) -> None:
        """Process and route an incoming message."""
        msg_type = message.type
        logger.debug(
            f"Message received: type={msg_type} from={message.source} "
            f"target={message.target} topic={message.topic}"
        )

        # Update heartbeat time on any message
        client.last_heartbeat = time.time()

        # Handle Internal Bus Protocol messages
        if msg_type == MessageType.BUS_REGISTER.value:
            new_id = message.payload.get("agent_id") or message.source
            metadata = message.payload.get("metadata", {})
            subs = message.payload.get("subscriptions", [])

            async with self._lock:
                if client.client_id in self._clients and self._clients[client.client_id] is client:
                    del self._clients[client.client_id]
                client.client_id = new_id
                client.metadata.update(metadata)
                for s in subs:
                    client.subscriptions.add(s)
                self._clients[new_id] = client

            logger.info(f"Agent registered: '{new_id}' with subscriptions={list(client.subscriptions)}")
            ack = AgentMessage(
                type=MessageType.BUS_ACK.value,
                source="bus_server",
                target=new_id,
                reply_to=message.msg_id,
                payload={"status": "registered", "agent_id": new_id},
            )
            await client.send(ack)

            # Broadcast agent online notice to other subscribers
            await self.broadcast(
                AgentMessage(
                    type=MessageType.AGENT_ONLINE.value,
                    source=new_id,
                    payload={"agent_id": new_id, "metadata": client.metadata},
                ),
                exclude=client,
            )
            return

        elif msg_type == MessageType.BUS_SUBSCRIBE.value:
            topics = message.payload.get("topics", [])
            if isinstance(topics, str):
                topics = [topics]
            for t in topics:
                client.subscriptions.add(t)
            logger.debug(f"Agent '{client.client_id}' subscribed to: {topics}")
            ack = AgentMessage(
                type=MessageType.BUS_ACK.value,
                source="bus_server",
                target=client.client_id,
                reply_to=message.msg_id,
                payload={"status": "subscribed", "subscriptions": list(client.subscriptions)},
            )
            await client.send(ack)
            return

        elif msg_type == MessageType.BUS_UNSUBSCRIBE.value:
            topics = message.payload.get("topics", [])
            if isinstance(topics, str):
                topics = [topics]
            for t in topics:
                client.subscriptions.discard(t)
            ack = AgentMessage(
                type=MessageType.BUS_ACK.value,
                source="bus_server",
                target=client.client_id,
                reply_to=message.msg_id,
                payload={"status": "unsubscribed", "subscriptions": list(client.subscriptions)},
            )
            await client.send(ack)
            return

        elif msg_type == MessageType.BUS_PING.value:
            pong = AgentMessage(
                type=MessageType.BUS_PONG.value,
                source="bus_server",
                target=client.client_id,
                reply_to=message.msg_id,
                payload={"time": time.time()},
            )
            await client.send(pong)
            return

        elif msg_type == MessageType.AGENT_HEARTBEAT.value:
            client.metadata.update(message.payload.get("stats", {}))
            # Forward heartbeat to monitoring subscribers (like CEO/Dashboard)
            await self.route_message(message, sender=client)

        else:
            # Route domain messages (task.assign, task.progress, task.complete, task.failed, task.cancel, custom topics)
            await self.route_message(message, sender=client)

        # Trigger registered server-side hooks
        await self._trigger_handlers(message, client)

    async def _trigger_handlers(self, message: AgentMessage, client: ConnectedClient) -> None:
        """Invoke server hooks registered for this message."""
        handlers_to_run = []
        for pattern, handlers in self._handlers.items():
            if topic_matches(pattern, message.type) or (message.topic and topic_matches(pattern, message.topic)):
                handlers_to_run.extend(handlers)

        for handler in handlers_to_run:
            try:
                res = handler(message, client)
                if asyncio.iscoroutine(res):
                    await res
            except Exception as e:
                logger.error(f"Error executing server handler for {message.type}: {e}", exc_info=True)

    async def route_message(
        self,
        message: AgentMessage,
        sender: Optional[ConnectedClient] = None,
    ) -> int:
        """Route message based on target or topic subscriptions.

        Returns number of clients the message was delivered to.
        """
        delivered_count = 0

        # Direct point-to-point delivery if target specified
        if message.target and message.target not in ("*", "broadcast", "all"):
            target_client = self._clients.get(message.target)
            if target_client:
                sent = await target_client.send(message)
                if sent:
                    delivered_count += 1
            else:
                logger.debug(f"Target client '{message.target}' not connected for message {message.msg_id}")
            return delivered_count

        # Pub/Sub topic-based routing
        topic_to_match = message.topic or message.type
        recipients: Set[ConnectedClient] = set()

        for c in self._all_clients:
            if sender and c is sender:
                continue  # Do not echo back to sender by default

            # Check if any client subscription matches
            for sub in c.subscriptions:
                if topic_matches(sub, topic_to_match) or topic_matches(sub, message.type):
                    recipients.add(c)
                    break

        for recipient in recipients:
            sent = await recipient.send(message)
            if sent:
                delivered_count += 1

        return delivered_count

    async def broadcast(
        self,
        message: AgentMessage,
        exclude: Optional[ConnectedClient] = None,
    ) -> int:
        """Broadcast message to all connected clients."""
        delivered_count = 0
        for c in list(self._all_clients):
            if exclude and c is exclude:
                continue
            if await c.send(message):
                delivered_count += 1
        return delivered_count

    async def _remove_client(self, client: ConnectedClient) -> None:
        """Clean up when a client disconnects."""
        async with self._lock:
            self._all_clients.discard(client)
            if client.client_id in self._clients and self._clients[client.client_id] is client:
                del self._clients[client.client_id]

        try:
            if not client.writer.is_closing():
                client.writer.close()
                await client.writer.wait_closed()
        except Exception:
            pass

        logger.info(f"Client disconnected: '{client.client_id}'")

        # Broadcast offline notification if it was an identified agent
        if client.client_id != "anonymous" and self._running:
            await self.broadcast(
                AgentMessage(
                    type=MessageType.AGENT_OFFLINE.value,
                    source=client.client_id,
                    payload={"agent_id": client.client_id},
                )
            )

    async def _monitor_heartbeats(self, check_interval: float = 15.0, timeout: float = 60.0) -> None:
        """Background task checking for stale/dead agents."""
        while self._running:
            try:
                await asyncio.sleep(check_interval)
                now = time.time()
                stale_clients = [
                    c for c in list(self._all_clients)
                    if c.client_id != "anonymous" and (now - c.last_heartbeat) > timeout
                ]
                for client in stale_clients:
                    logger.warning(
                        f"Agent '{client.client_id}' timed out "
                        f"(no heartbeat for {now - client.last_heartbeat:.1f}s). Disconnecting..."
                    )
                    await self._remove_client(client)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in heartbeat monitor: {e}", exc_info=True)


class AgentBusClient:
    """High-level async client for agents communicating over the Jarvis Agent Bus."""

    def __init__(
        self,
        agent_id: str,
        socket_path: str = DEFAULT_SOCKET_PATH,
        auto_reconnect: bool = True,
        reconnect_interval: float = 2.0,
    ):
        self.agent_id = agent_id
        self.socket_path = socket_path
        self.auto_reconnect = auto_reconnect
        self.reconnect_interval = reconnect_interval

        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = False
        self._closing = False
        self._subscriptions: Set[str] = set()
        self._handlers: Dict[str, List[Callable[[AgentMessage], Any]]] = {}
        self._pending_responses: Dict[str, asyncio.Future] = {}
        self._listen_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._lock = asyncio.Lock()

    @property
    def is_connected(self) -> bool:
        return self._connected and self._writer is not None and not self._writer.is_closing()

    async def connect(self) -> None:
        """Connect to the Unix Domain Socket broker and register identity."""
        if self.is_connected:
            return

        self._closing = False
        logger.debug(f"[{self.agent_id}] Connecting to {self.socket_path}...")
        try:
            self._reader, self._writer = await asyncio.open_unix_connection(path=self.socket_path)
            self._connected = True
            logger.info(f"[{self.agent_id}] Connected to Jarvis Agent Bus at {self.socket_path}")

            # Start message reading loop
            if self._listen_task is None or self._listen_task.done():
                self._listen_task = asyncio.create_task(self._listen_loop())

            # Register with broker
            reg_msg = AgentMessage(
                type=MessageType.BUS_REGISTER.value,
                source=self.agent_id,
                payload={
                    "agent_id": self.agent_id,
                    "subscriptions": list(self._subscriptions),
                },
            )
            await self._send_raw(reg_msg)

        except Exception as e:
            self._connected = False
            logger.error(f"[{self.agent_id}] Connection failed to {self.socket_path}: {e}")
            raise

    async def close(self) -> None:
        """Disconnect and clean up resources."""
        self._closing = True
        self._connected = False

        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None

        if self._listen_task:
            self._listen_task.cancel()
            self._listen_task = None

        if self._writer:
            try:
                self._writer.close()
                await self._writer.wait_closed()
            except Exception:
                pass
            self._writer = None
            self._reader = None

        # Fail any pending futures
        for fut in self._pending_responses.values():
            if not fut.done():
                fut.cancel()
        self._pending_responses.clear()
        logger.info(f"[{self.agent_id}] Disconnected from agent bus")

    async def __aenter__(self) -> "AgentBusClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _send_raw(self, message: AgentMessage) -> bool:
        """Internal helper to write raw message to socket."""
        async with self._lock:
            if not self.is_connected or not self._writer:
                return False
            try:
                self._writer.write(message.to_bytes())
                await self._writer.drain()
                return True
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error sending message: {e}")
                self._connected = False
                return False

    async def publish(
        self,
        msg_type: Union[MessageType, str],
        payload: Optional[Dict[str, Any]] = None,
        target: Optional[str] = None,
        topic: Optional[str] = None,
        reply_to: Optional[str] = None,
    ) -> AgentMessage:
        """Publish a message over the bus."""
        type_str = msg_type.value if isinstance(msg_type, MessageType) else str(msg_type)
        msg = AgentMessage(
            type=type_str,
            source=self.agent_id,
            target=target,
            topic=topic or type_str,
            payload=payload or {},
            reply_to=reply_to,
        )
        success = await self._send_raw(msg)
        if not success:
            raise ConnectionError(f"Failed to publish message {type_str}: client disconnected")
        return msg

    async def request(
        self,
        msg_type: Union[MessageType, str],
        payload: Optional[Dict[str, Any]] = None,
        target: Optional[str] = None,
        timeout: float = 10.0,
    ) -> AgentMessage:
        """Send a request message and await a correlated reply."""
        type_str = msg_type.value if isinstance(msg_type, MessageType) else str(msg_type)
        msg = AgentMessage(
            type=type_str,
            source=self.agent_id,
            target=target,
            topic=type_str,
            payload=payload or {},
        )

        future = asyncio.get_running_loop().create_future()
        self._pending_responses[msg.msg_id] = future

        try:
            await self._send_raw(msg)
            return await asyncio.wait_for(future, timeout=timeout)
        finally:
            self._pending_responses.pop(msg.msg_id, None)

    async def subscribe(
        self,
        topics: Union[str, List[str]],
        callback: Optional[Callable[[AgentMessage], Any]] = None,
    ) -> None:
        """Subscribe to topic(s) with optional callback handler."""
        if isinstance(topics, str):
            topics = [topics]

        for t in topics:
            self._subscriptions.add(t)
            if callback:
                self.on(t, callback)

        if self.is_connected:
            msg = AgentMessage(
                type=MessageType.BUS_SUBSCRIBE.value,
                source=self.agent_id,
                payload={"topics": list(topics)},
            )
            await self._send_raw(msg)

    async def unsubscribe(self, topics: Union[str, List[str]]) -> None:
        """Unsubscribe from topic(s)."""
        if isinstance(topics, str):
            topics = [topics]

        for t in topics:
            self._subscriptions.discard(t)

        if self.is_connected:
            msg = AgentMessage(
                type=MessageType.BUS_UNSUBSCRIBE.value,
                source=self.agent_id,
                payload={"topics": list(topics)},
            )
            await self._send_raw(msg)

    def on(self, msg_type_or_pattern: Union[MessageType, str], handler: Callable[[AgentMessage], Any]) -> None:
        """Register a handler for a message type or topic pattern."""
        key = msg_type_or_pattern.value if isinstance(msg_type_or_pattern, MessageType) else str(msg_type_or_pattern)
        self._handlers.setdefault(key, []).append(handler)

    # --------------------------------------------------------------------------
    # Specialized Task and Heartbeat Helper Methods
    # --------------------------------------------------------------------------

    async def send_task_assign(
        self,
        target: str,
        task_id: str,
        task_type: str,
        params: Dict[str, Any],
        title: str = "",
        timeout: Optional[float] = None,
    ) -> AgentMessage:
        """Assign a task to a worker agent (e.g. Paperclip, Friday, Ultron)."""
        payload = {
            "task_id": task_id,
            "task_type": task_type,
            "title": title,
            "params": params,
            "timeout": timeout,
        }
        return await self.publish(
            msg_type=MessageType.TASK_ASSIGN,
            payload=payload,
            target=target,
            topic=MessageType.TASK_ASSIGN.value,
        )

    async def send_task_progress(
        self,
        task_id: str,
        progress: float,
        status: str,
        details: Optional[Dict[str, Any]] = None,
        target: Optional[str] = None,
    ) -> AgentMessage:
        """Publish task execution progress (0.0 to 1.0)."""
        payload = {
            "task_id": task_id,
            "progress": progress,
            "status": status,
            "details": details or {},
        }
        return await self.publish(
            msg_type=MessageType.TASK_PROGRESS,
            payload=payload,
            target=target,
            topic=MessageType.TASK_PROGRESS.value,
        )

    async def send_task_complete(
        self,
        task_id: str,
        result: Any,
        summary: str = "",
        target: Optional[str] = None,
    ) -> AgentMessage:
        """Notify that a task completed successfully."""
        payload = {
            "task_id": task_id,
            "result": result,
            "summary": summary,
            "status": "completed",
        }
        return await self.publish(
            msg_type=MessageType.TASK_COMPLETE,
            payload=payload,
            target=target,
            topic=MessageType.TASK_COMPLETE.value,
        )

    async def send_task_failed(
        self,
        task_id: str,
        error: str,
        traceback_str: Optional[str] = None,
        target: Optional[str] = None,
    ) -> AgentMessage:
        """Notify that a task failed with an error."""
        payload = {
            "task_id": task_id,
            "error": error,
            "traceback": traceback_str,
            "status": "failed",
        }
        return await self.publish(
            msg_type=MessageType.TASK_FAILED,
            payload=payload,
            target=target,
            topic=MessageType.TASK_FAILED.value,
        )

    async def send_task_cancel(
        self,
        task_id: str,
        reason: str = "User requested cancellation",
        target: Optional[str] = None,
    ) -> AgentMessage:
        """Request cancellation of an active task."""
        payload = {
            "task_id": task_id,
            "reason": reason,
        }
        return await self.publish(
            msg_type=MessageType.TASK_CANCEL,
            payload=payload,
            target=target,
            topic=MessageType.TASK_CANCEL.value,
        )

    async def send_heartbeat(
        self,
        status: str = "online",
        stats: Optional[Dict[str, Any]] = None,
    ) -> AgentMessage:
        """Send agent health and status heartbeat."""
        payload = {
            "status": status,
            "stats": stats or {},
            "timestamp": time.time(),
        }
        return await self.publish(
            msg_type=MessageType.AGENT_HEARTBEAT,
            payload=payload,
            topic=MessageType.AGENT_HEARTBEAT.value,
        )

    def start_heartbeat_loop(self, interval: float = 10.0, stats_provider: Optional[Callable[[], dict]] = None) -> None:
        """Start a background task sending periodic heartbeats."""
        if self._heartbeat_task and not self._heartbeat_task.done():
            return

        async def _loop():
            while not self._closing:
                try:
                    if self.is_connected:
                        stats = stats_provider() if stats_provider else {}
                        await self.send_heartbeat(status="online", stats=stats)
                    await asyncio.sleep(interval)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.debug(f"[{self.agent_id}] Heartbeat error: {e}")
                    await asyncio.sleep(interval)

        self._heartbeat_task = asyncio.create_task(_loop())

    # --------------------------------------------------------------------------
    # Internal Listening and Reconnection Loop
    # --------------------------------------------------------------------------

    async def _listen_loop(self) -> None:
        """Read and dispatch messages from the broker."""
        while not self._closing:
            try:
                if not self._reader:
                    await asyncio.sleep(0.5)
                    continue

                line = await self._reader.readline()
                if not line:
                    logger.warning(f"[{self.agent_id}] Connection lost to broker")
                    self._connected = False
                    if self.auto_reconnect and not self._closing:
                        await self._reconnect_loop()
                    break

                try:
                    msg = AgentMessage.from_json(line)
                except Exception as e:
                    logger.warning(f"[{self.agent_id}] Malformed incoming message: {e}")
                    continue

                # Check if this resolves a pending request() future
                if msg.reply_to and msg.reply_to in self._pending_responses:
                    fut = self._pending_responses[msg.reply_to]
                    if not fut.done():
                        fut.set_result(msg)

                # Dispatch to matching handlers
                await self._dispatch_message(msg)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error in client listen loop: {e}")
                if self.auto_reconnect and not self._closing:
                    await self._reconnect_loop()
                break

    async def _dispatch_message(self, message: AgentMessage) -> None:
        """Dispatch received message to registered callback handlers."""
        handlers_to_run = []
        for pattern, handlers in self._handlers.items():
            if topic_matches(pattern, message.type) or (message.topic and topic_matches(pattern, message.topic)):
                handlers_to_run.extend(handlers)

        for handler in handlers_to_run:
            try:
                res = handler(message)
                if asyncio.iscoroutine(res):
                    await res
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error in message handler for {message.type}: {e}", exc_info=True)

    async def _reconnect_loop(self) -> None:
        """Attempt to reconnect to broker periodically."""
        logger.info(f"[{self.agent_id}] Starting reconnection loop...")
        while not self._closing and not self.is_connected:
            try:
                await asyncio.sleep(self.reconnect_interval)
                logger.debug(f"[{self.agent_id}] Attempting reconnect...")
                await self.connect()
                logger.info(f"[{self.agent_id}] Reconnected successfully!")
                return
            except Exception:
                pass


# ------------------------------------------------------------------------------
# CLI and Daemon runner
# ------------------------------------------------------------------------------


def setup_logging(verbose: bool = False) -> None:
    """Configure structured console logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def run_server_daemon(socket_path: str = DEFAULT_SOCKET_PATH) -> None:
    """Run the AgentBusServer as a standalone daemon with signal handlers."""
    server = AgentBusServer(socket_path=socket_path)
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def _sig_handler():
        logger.info("Signal received, initiating graceful shutdown...")
        stop_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _sig_handler)
        except NotImplementedError:
            # Fallback for platforms without add_signal_handler support
            pass

    async with server:
        logger.info("Agent bus server running. Press Ctrl+C to terminate.")
        await stop_event.wait()
    logger.info("Agent bus server stopped cleanly.")


def main() -> None:
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser(description="Jarvis OS Agent Bus UNIX Domain Socket Broker & CLI")
    parser.add_argument("--socket", default=DEFAULT_SOCKET_PATH, help="Path to UNIX domain socket")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug logging")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Server command
    subparsers.add_parser("server", help="Run the Agent Bus broker server daemon")

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Subscribe and monitor all messages on the bus")
    monitor_parser.add_argument("--pattern", default="*", help="Topic pattern to subscribe to (default: '*')")

    # Send command
    send_parser = subparsers.add_parser("send", help="Send a test message on the bus")
    send_parser.add_argument("--type", required=True, help="Message type (e.g. task.assign, agent.heartbeat)")
    send_parser.add_argument("--source", default="cli_tool", help="Source agent ID")
    send_parser.add_argument("--target", default=None, help="Target agent ID")
    send_parser.add_argument("--payload", default="{}", help="JSON payload string")

    args = parser.parse_args()
    setup_logging(verbose=args.verbose)

    if args.command == "server" or args.command is None:
        try:
            asyncio.run(run_server_daemon(socket_path=args.socket))
        except KeyboardInterrupt:
            pass
    elif args.command == "monitor":
        async def _run_monitor():
            async with AgentBusClient(agent_id="monitor_cli", socket_path=args.socket) as client:
                print(f"Monitoring messages on {args.socket} with pattern '{args.pattern}'...")

                def _print_msg(msg: AgentMessage):
                    print(f"[{time.strftime('%H:%M:%S')}] [{msg.type}] from={msg.source} to={msg.target} | {msg.payload}")

                await client.subscribe(args.pattern, _print_msg)
                try:
                    while True:
                        await asyncio.sleep(1)
                except asyncio.CancelledError:
                    pass

        try:
            asyncio.run(_run_monitor())
        except KeyboardInterrupt:
            pass
    elif args.command == "send":
        async def _run_send():
            async with AgentBusClient(agent_id=args.source, socket_path=args.socket) as client:
                payload = json.loads(args.payload)
                msg = await client.publish(msg_type=args.type, payload=payload, target=args.target)
                print(f"Sent message {msg.msg_id} ({args.type}) -> {msg.target or 'broadcast'}")

        asyncio.run(_run_send())


if __name__ == "__main__":
    main()
