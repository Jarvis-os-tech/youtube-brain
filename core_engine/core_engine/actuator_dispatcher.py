"""
Omarchy Wayland Actuator Dispatcher
Provides wrapper functions for underlying OS Wayland commands.
"""
import subprocess
import logging

logger = logging.getLogger(__name__)

def _run_cmd(cmd: list) -> str:
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return res.stdout.strip() if res.stdout else "Success"
    except subprocess.CalledProcessError as e:
        err = f"Command failed ({e.returncode}): {' '.join(cmd)}\n{e.stderr.strip()}"
        logger.error(err)
        return err
    except FileNotFoundError:
        err = f"Command not found: {cmd[0]}"
        logger.error(err)
        return err
    except Exception as e:
        err = f"Unexpected error: {e}"
        logger.error(err)
        return err

def window_control(action: str, arg: str = "") -> str:
    """Control window via hyprctl dispatch (e.g. closewindow, focuswindow)."""
    cmd = ["hyprctl", "dispatch", action]
    if arg:
        cmd.append(arg)
    return _run_cmd(cmd)

def workspace_control(workspace: str) -> str:
    """Switch to or control workspace via hyprctl dispatch workspace."""
    return _run_cmd(["hyprctl", "dispatch", "workspace", workspace])

def screenshot(output_path: str, region: bool = False) -> str:
    """Take a screenshot using grim and optionally slurp."""
    if region:
        try:
            slurp = subprocess.run(["slurp"], check=True, capture_output=True, text=True)
            geom = slurp.stdout.strip()
            return _run_cmd(["grim", "-g", geom, output_path])
        except subprocess.CalledProcessError:
            return "Screenshot region selection cancelled or failed."
    else:
        return _run_cmd(["grim", output_path])

def spawn_terminal(app: str = "foot", cmd_args: list | None = None) -> str:
    """Spawn terminal (foot or ghostty)."""
    if app not in ["foot", "ghostty"]:
        return f"Unsupported terminal: {app}"
    cmd = [app]
    if cmd_args:
        cmd.extend(cmd_args)
    try:
        # spawn in a detached session so it doesn't block the caller
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        return f"Spawned {app}"
    except Exception as e:
        err = f"Failed to spawn {app}: {e}"
        logger.error(err)
        return err

def volume(action: str, amount: str = "") -> str:
    """Control volume via wpctl (action: set-volume, set-mute)."""
    cmd = ["wpctl", action, "@DEFAULT_AUDIO_SINK@"]
    if amount:
        cmd.append(amount)
    return _run_cmd(cmd)

def brightness(amount: str) -> str:
    """Control brightness via brightnessctl."""
    return _run_cmd(["brightnessctl", "set", amount])

def omarchy(action: str, arg: str = "") -> str:
    """Omarchy system controls (theme, toggle, restart)."""
    if action not in ["theme", "toggle", "restart"]:
        return f"Unsupported omarchy action: {action}"
    cmd = ["omarchy", action]
    if arg:
        cmd.append(arg)
    return _run_cmd(cmd)
