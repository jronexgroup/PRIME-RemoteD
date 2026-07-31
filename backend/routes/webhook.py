from fastapi import APIRouter, Request
from auth import is_authorized_telegram_user
from telegram import (
    send_message, answer_callback_query,
    build_main_menu, build_power_menu, build_volume_menu,
    build_clipboard_menu, build_apps_menu, build_keyboard_menu,
    build_mouse_menu, build_record_menu, build_files_menu,
)
from services.command_queue import device_manager, Command
import logging

logger = logging.getLogger("backend.webhook")
router = APIRouter()


async def broadcast_command(cmd_type: str, chat_id: int, callback_id: str, label: str, args: dict = None):
    devices = device_manager.get_devices()
    if not devices:
        await send_message(chat_id, "No devices connected.")
        await answer_callback_query(callback_id, "No devices")
        return
    for device_id in devices:
        devices[device_id]["chat_id"] = chat_id
        cmd = Command(type=cmd_type, device_id=device_id, args=args or {})
        await device_manager.enqueue_command(device_id, cmd)
    await send_message(chat_id, f"{label}")
    await answer_callback_query(callback_id)


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()

    if "callback_query" in data:
        return await handle_callback(data["callback_query"])

    if "message" in data:
        return await handle_message(data["message"])

    return {"ok": True}


async def handle_message(message: dict) -> dict:
    user_id = message.get("from", {}).get("id")
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not is_authorized_telegram_user(user_id):
        return {"ok": True}

    if text == "/start":
        await send_message(chat_id, "🖥 PRIME REMOTE D\nSelect an option:", build_main_menu())
    elif text == "/help":
        await send_message(chat_id, "Use the menu buttons to control your PC.")
    else:
        await handle_text_input(chat_id, text)

    return {"ok": True}


async def handle_text_input(chat_id: int, text: str):
    devices = device_manager.get_devices()
    device_id = list(devices.keys())[0] if devices else None
    if not device_id:
        return

    info = devices.get(device_id, {})
    pending = info.get("pending_action")

    if pending == "open_url":
        cmd = Command(type="open_url", device_id=device_id, args={"url": text})
        await device_manager.enqueue_command(device_id, cmd)
        await send_message(chat_id, f"🌐 Opening: {text}")
        info["pending_action"] = None

    elif pending == "open_app":
        cmd = Command(type="open_app", device_id=device_id, args={"app": text})
        await device_manager.enqueue_command(device_id, cmd)
        await send_message(chat_id, f"📱 Opening: {text}")
        info["pending_action"] = None

    elif pending == "terminal":
        cmd = Command(type="terminal", device_id=device_id, args={"command": text})
        await device_manager.enqueue_command(device_id, cmd)
        await send_message(chat_id, f"💻 Running: {text}")
        info["pending_action"] = None

    elif pending == "keyboard":
        cmd = Command(type="keyboard", device_id=device_id, args={"key": text})
        await device_manager.enqueue_command(device_id, cmd)
        await send_message(chat_id, f"⌨️ Pressing: {text}")
        info["pending_action"] = None

    elif pending == "mouse_click":
        try:
            parts = text.split(",")
            x, y = int(parts[0].strip()), int(parts[1].strip())
            cmd = Command(type="mouse_click", device_id=device_id, args={"x": x, "y": y})
            await device_manager.enqueue_command(device_id, cmd)
            await send_message(chat_id, f"🖱 Clicking at ({x}, {y})")
        except (ValueError, IndexError):
            await send_message(chat_id, "Invalid format. Send: x,y (e.g. 500,300)")
        info["pending_action"] = None

    else:
        await send_message(chat_id, "Use the menu buttons to control your PC.")


async def handle_callback(callback_query: dict) -> dict:
    user_id = callback_query.get("from", {}).get("id")
    chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
    callback_id = callback_query.get("id", "")
    data = callback_query.get("data", "")

    if not is_authorized_telegram_user(user_id):
        await answer_callback_query(callback_id, "Unauthorized")
        return {"ok": True}

    devices = device_manager.get_devices()
    device_id = list(devices.keys())[0] if devices else None
    if device_id:
        devices[device_id]["chat_id"] = chat_id

    if data == "main_menu":
        await send_message(chat_id, "🖥 PRIME REMOTE D\nSelect an option:", build_main_menu())

    elif data == "power":
        await send_message(chat_id, "⚡ Power Menu\nSelect action:", build_power_menu())
    elif data == "power_shutdown":
        await broadcast_command("shutdown", chat_id, callback_id, "🔴 Shutdown command sent.")
    elif data == "power_restart":
        await broadcast_command("restart", chat_id, callback_id, "🟡 Restart command sent.")
    elif data == "power_sleep":
        await broadcast_command("sleep", chat_id, callback_id, "🔵 Sleep command sent.")
    elif data == "power_lock":
        await broadcast_command("lock", chat_id, callback_id, "🟢 Lock command sent.")

    elif data == "screenshot":
        await broadcast_command("screenshot", chat_id, callback_id, "📸 Screenshot requested...")
    elif data == "system":
        await broadcast_command("system_info", chat_id, callback_id, "📊 Fetching system info...")

    elif data == "volume":
        await send_message(chat_id, "🔊 Volume Menu:", build_volume_menu())
    elif data == "volume_up":
        await broadcast_command("volume_up", chat_id, callback_id, "🔊 Volume increased.")
    elif data == "volume_down":
        await broadcast_command("volume_down", chat_id, callback_id, "🔉 Volume decreased.")
    elif data == "volume_mute":
        await broadcast_command("volume_mute", chat_id, callback_id, "🔇 Muted.")
    elif data == "volume_unmute":
        await broadcast_command("volume_unmute", chat_id, callback_id, "🔊 Unmuted.")

    elif data == "clipboard":
        await send_message(chat_id, "📋 Clipboard Menu:", build_clipboard_menu())
    elif data == "clipboard_get":
        await broadcast_command("clipboard_get", chat_id, callback_id, "📋 Fetching clipboard...")

    elif data == "apps":
        await send_message(chat_id, "🌐 Apps Menu:", build_apps_menu())
    elif data == "open_url":
        if device_id:
            devices[device_id]["pending_action"] = "open_url"
        await send_message(chat_id, "Send me the URL to open:")
        await answer_callback_query(callback_id)
    elif data == "open_app":
        if device_id:
            devices[device_id]["pending_action"] = "open_app"
        await send_message(chat_id, "Send me the app name (e.g. notepad):")
        await answer_callback_query(callback_id)

    elif data == "keyboard":
        await send_message(chat_id, "⌨️ Keyboard Menu:", build_keyboard_menu())
    elif data.startswith("key_"):
        key = data.replace("key_", "")
        await broadcast_command("keyboard", chat_id, callback_id, f"⌨️ Pressed: {key}", {"key": key})

    elif data == "mouse":
        await send_message(chat_id, "🖱 Mouse Menu:", build_mouse_menu())
    elif data == "mouse_click_mode":
        if device_id:
            devices[device_id]["pending_action"] = "mouse_click"
        await send_message(chat_id, "Send coordinates as x,y (e.g. 500,300):")
        await answer_callback_query(callback_id)
    elif data == "mouse_scroll_up":
        await broadcast_command("mouse_scroll", chat_id, callback_id, "🔄 Scrolled up", {"dx": 0, "dy": 3})
    elif data == "mouse_scroll_down":
        await broadcast_command("mouse_scroll", chat_id, callback_id, "🔄 Scrolled down", {"dx": 0, "dy": -3})

    elif data == "terminal":
        if device_id:
            devices[device_id]["pending_action"] = "terminal"
        await send_message(chat_id, "💻 Send a command:\nAllowed: dir, ipconfig, ping, systeminfo, tasklist, whoami")
        await answer_callback_query(callback_id)

    elif data == "scripts":
        await broadcast_command("list_scripts", chat_id, callback_id, "📜 Listing scripts...")
    elif data.startswith("run_script:"):
        script = data.split(":", 1)[1]
        await broadcast_command("run_script", chat_id, callback_id, f"📜 Running: {script}", {"script": script})

    elif data == "record":
        await send_message(chat_id, "🎬 Screen Recording:", build_record_menu())
    elif data.startswith("record_"):
        duration = int(data.split("_")[1])
        await broadcast_command("record_screen", chat_id, callback_id, f"🎬 Recording {duration}s...", {"duration": duration})

    elif data == "upload":
        await send_message(chat_id, "📤 Send me a file to upload to your PC:")

    elif data == "devices":
        if devices:
            device_list = "\n".join([f"- {did}: {info.get('name', 'Unknown')}" for did, info in devices.items()])
            await send_message(chat_id, f"🖥 Connected Devices:\n{device_list}")
        else:
            await send_message(chat_id, "No devices connected.")
        await answer_callback_query(callback_id)

    else:
        await answer_callback_query(callback_id, "Unknown action")

    return {"ok": True}
