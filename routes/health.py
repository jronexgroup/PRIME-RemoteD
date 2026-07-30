from fastapi import APIRouter
from services.command_queue import device_manager

router = APIRouter()


@router.get("/health")
async def health_check():
    devices = device_manager.get_devices()
    return {
        "status": "healthy",
        "service": "PRIME REMOTE D",
        "version": "1.0.0",
        "connected_devices": len(devices),
    }


@router.get("/set-webhook")
async def set_webhook():
    from config import settings
    import httpx

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
    webhook_url = "http://127.0.0.1:8000/telegram/webhook"

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={"url": webhook_url})
        return resp.json()
