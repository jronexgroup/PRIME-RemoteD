from fastapi import APIRouter, Request
from auth import is_authorized_telegram_user
from telegram import send_message, answer_callback_query, build_main_menu, build_power_menu
from services.command_queue import device_manager, Command
import logging

logger = logging.getLogger("backend.webhook")
router = APIRouter()

DEVICE_ID = "home-pc"


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
        logger.warning(f"Unauthorized user: {user_id}")
        return {"ok": True}

    if text == "/start":
        await send_message(chat_id, "🖥 PRIME REMOTE D\nSelect an option:", build_main_menu())
    elif text == "/help":
        await send_message(chat_id, "Commands:\n/start - Main menu\n/help - Show help")
    else:
        await send_message(chat_id, "Use the menu buttons to control your PC.")

    return {"ok": True}


async def handle_callback(callback_query: dict) -> dict:
    user_id = callback_query.get("from", {}).get("id")
    chat_id = callback_query.get("message", {}).get("chat", {}).get("id")
    callback_id = callback_query.get("id", "")
    data = callback_query.get("data", "")

    if not is_authorized_telegram_user(user_id):
        await answer_callback_query(callback_id, "Unauthorized")
        return {"ok": True}

    if data == "main_menu":
        await send_message(chat_id, "🖥 PRIME REMOTE D\nSelect an option:", build_main_menu())

    elif data == "power":
        await send_message(chat_id, "⚡ Power Menu\nSelect action:", build_power_menu())

    elif data == "power_shutdown":
        cmd = Command(type="shutdown", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "🔴 Shutdown command sent.")
        await answer_callback_query(callback_id, "Shutdown sent")

    elif data == "power_restart":
        cmd = Command(type="restart", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "🟡 Restart command sent.")
        await answer_callback_query(callback_id, "Restart sent")

    elif data == "power_sleep":
        cmd = Command(type="sleep", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "🔵 Sleep command sent.")
        await answer_callback_query(callback_id, "Sleep sent")

    elif data == "power_lock":
        cmd = Command(type="lock", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "🟢 Lock command sent.")
        await answer_callback_query(callback_id, "Lock sent")

    elif data == "screenshot":
        cmd = Command(type="screenshot", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "📸 Screenshot requested...")
        await answer_callback_query(callback_id, "Screenshot requested")

    elif data == "system":
        cmd = Command(type="system_info", device_id=DEVICE_ID)
        await device_manager.enqueue_command(DEVICE_ID, cmd)
        await send_message(chat_id, "📊 Fetching system info...")
        await answer_callback_query(callback_id, "System info requested")

    elif data == "devices":
        devices = device_manager.get_devices()
        if devices:
            device_list = "\n".join([f"- {did}: {info.get('name', 'Unknown')}" for did, info in devices.items()])
            await send_message(chat_id, f"🖥 Connected Devices:\n{device_list}")
        else:
            await send_message(chat_id, "No devices connected.")
        await answer_callback_query(callback_id)

    else:
        await answer_callback_query(callback_id, "Unknown action")

    return {"ok": True}
