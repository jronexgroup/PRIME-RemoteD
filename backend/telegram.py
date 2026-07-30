import httpx
from config import settings

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}"


async def send_message(chat_id: int, text: str, reply_markup: dict | None = None) -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload)
        return resp.status_code == 200


async def send_photo(chat_id: int, photo: bytes, caption: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/sendPhoto"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": ("screenshot.png", photo, "image/png")},
        )
        return resp.status_code == 200


async def answer_callback_query(callback_query_id: str, text: str = "") -> bool:
    url = f"{TELEGRAM_API_BASE.format(token=settings.TELEGRAM_BOT_TOKEN)}/answerCallbackQuery"
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"callback_query_id": callback_query_id, "text": text})
        return resp.status_code == 200


def build_main_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "🖥 Devices", "callback_data": "devices"}],
            [
                {"text": "⚡ Power", "callback_data": "power"},
                {"text": "📸 Screenshot", "callback_data": "screenshot"},
            ],
            [
                {"text": "📂 Files", "callback_data": "files"},
                {"text": "📋 Clipboard", "callback_data": "clipboard"},
            ],
            [
                {"text": "🔊 Volume", "callback_data": "volume"},
                {"text": "⚙ System", "callback_data": "system"},
            ],
        ]
    }


def build_power_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔴 Shutdown", "callback_data": "power_shutdown"},
                {"text": "🟡 Restart", "callback_data": "power_restart"},
            ],
            [
                {"text": "🔵 Sleep", "callback_data": "power_sleep"},
                {"text": "🟢 Lock", "callback_data": "power_lock"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_volume_menu() -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": "🔊 Volume Up", "callback_data": "volume_up"},
                {"text": "🔉 Volume Down", "callback_data": "volume_down"},
            ],
            [
                {"text": "🔇 Mute", "callback_data": "volume_mute"},
                {"text": "🔊 Unmute", "callback_data": "volume_unmute"},
            ],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }


def build_clipboard_menu() -> dict:
    return {
        "inline_keyboard": [
            [{"text": "📋 Get Clipboard", "callback_data": "clipboard_get"}],
            [{"text": "◀ Back", "callback_data": "main_menu"}],
        ]
    }
