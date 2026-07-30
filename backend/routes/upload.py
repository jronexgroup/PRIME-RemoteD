from fastapi import APIRouter, Request, UploadFile, File, Form
from telegram import send_photo, send_message
from services.command_queue import device_manager
import logging
import tempfile
import os

logger = logging.getLogger("backend.upload")
router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    device_id: str = Form(default=""),
    command_id: str = Form(default=""),
    file_type: str = Form(default="screenshot"),
):
    contents = await file.read()

    if file_type == "screenshot":
        for device_id_key, info in device_manager.get_devices().items():
            chat_id = info.get("chat_id")
            if chat_id:
                await send_photo(chat_id, contents, caption="📸 Screenshot from your PC")
                logger.info(f"Screenshot sent to chat {chat_id}")
                return {"ok": True, "message": "Screenshot sent to Telegram"}

    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    with open(temp_path, "wb") as f:
        f.write(contents)

    return {"ok": True, "message": f"File {file.filename} received"}
