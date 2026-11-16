#!/usr/bin/env python3
"""Loopback webhook that receives the Tampermonkey payload (Entry Point B).

Binds 127.0.0.1 only. Uses http.server from the standard library so the venv
stays free of web-framework dependencies.
"""

from __future__ import annotations

import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import config
import ingest

log = logging.getLogger("yt-brain-webhook")

MAX_BODY = 16 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "yt-brain/1.0"

    def _reply(self, code: int, body: dict) -> None:
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        # Loopback-only endpoint; allow the userscript's cross-origin POST.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._reply(200, {"ok": True, "buffer": str(config.BUFFER_FILE)})
        else:
            self._reply(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/webhook/watch":
            self._reply(404, {"ok": False, "error": "not found"})
            return

        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            self._reply(400, {"ok": False, "error": "bad content-length"})
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            self._reply(400, {"ok": False, "error": f"bad json: {exc}"})
            return

        if not isinstance(payload, dict) or not payload.get("url"):
            self._reply(400, {"ok": False, "error": "missing url"})
            return

        # Validate through the same parser the batch run uses, so a junk row
        # never reaches the queue.
        if ingest.video_id_from_url(payload["url"]) is None:
            self._reply(422, {"ok": False, "error": "not a youtube watch url"})
            return

        with config.BUFFER_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

        log.info("buffered %s | %s", payload.get("video_id"), payload.get("title", "")[:60])
        self._reply(200, {"ok": True})

    def log_message(self, fmt: str, *args) -> None:
        log.debug("%s - %s", self.address_string(), fmt % args)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[logging.FileHandler(config.LOG_DIR / "webhook.log", encoding="utf-8"), logging.StreamHandler()],
        force=True,
    )
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.BUFFER_FILE.touch(exist_ok=True)
    port = config.WEBHOOK_PORT
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    log.info("listening on http://127.0.0.1:%s (buffer: %s)", port, config.BUFFER_FILE)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("shutting down")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
