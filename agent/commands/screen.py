import os
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger("agent.screen")


async def execute_screenshot(cmd_type: str, args: dict) -> dict:
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "screenshot.png")
        screenshot.save(file_path, "PNG")

        from api import api
        await api.upload_file(file_path, "screenshot.png")

        return {"message": "Screenshot captured and sent.", "data": {"file_path": file_path}}
    except ImportError:
        return {"message": "Pillow not installed. Run: pip install pillow"}
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return {"message": f"Screenshot failed: {str(e)}"}
