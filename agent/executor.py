import logging
from commands.power import execute_power
from commands.screen import execute_screenshot
from commands.system import execute_system_info
from commands.volume import execute_volume
from commands.clipboard import execute_clipboard
from commands.apps import execute_open_url, execute_open_app
from commands.scripts import execute_list_scripts, execute_run_script
from commands.files import execute_list_dir, execute_file_info, execute_download_file
from commands.keyboard import execute_keyboard
from commands.mouse import execute_mouse
from commands.recording import execute_record_screen
from commands.terminal import execute_terminal

logger = logging.getLogger("agent.executor")

COMMAND_HANDLERS = {
    "shutdown": execute_power,
    "restart": execute_power,
    "sleep": execute_power,
    "lock": execute_power,
    "screenshot": execute_screenshot,
    "system_info": execute_system_info,
    "volume_up": execute_volume,
    "volume_down": execute_volume,
    "volume_mute": execute_volume,
    "volume_unmute": execute_volume,
    "clipboard_get": execute_clipboard,
    "clipboard_set": execute_clipboard,
    "open_url": execute_open_url,
    "open_app": execute_open_app,
    "list_scripts": execute_list_scripts,
    "run_script": execute_run_script,
    "list_dir": execute_list_dir,
    "file_info": execute_file_info,
    "download_file": execute_download_file,
    "keyboard": execute_keyboard,
    "mouse_move": execute_mouse,
    "mouse_click": execute_mouse,
    "mouse_double_click": execute_mouse,
    "mouse_scroll": execute_mouse,
    "mouse_click_sequence": execute_mouse,
    "mouse_preset": execute_mouse,
    "record_screen": execute_record_screen,
    "terminal": execute_terminal,
}


async def execute_command(cmd_type: str, args: dict) -> dict:
    handler = COMMAND_HANDLERS.get(cmd_type)
    if not handler:
        raise ValueError(f"Unsupported command: {cmd_type}")

    logger.info(f"Executing: {cmd_type} with args {args}")
    return await handler(cmd_type, args)
