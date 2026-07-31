import os
import tempfile
import logging

logger = logging.getLogger("agent.screen")


async def execute_screenshot(cmd_type: str, args: dict) -> dict:
    try:
        import mss
        import mss.tools

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "screenshot.png")
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=file_path)

        from api import api
        await api.upload_file(file_path, "screenshot.png")

        return {"message": "Screenshot captured and sent.", "data": {"file_path": file_path}}
    except ImportError:
        return {"message": "mss not installed. Run: pip install mss"}
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return {"message": f"Screenshot failed: {str(e)}"}
