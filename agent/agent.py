import asyncio
import sys
import signal
import base64
import io
from logger import setup_logger
from config import config
from api import api
from polling import start_polling

logger = setup_logger()

STREAM_ENABLED = True
STREAM_INTERVAL = 2


async def stream_screen():
    while STREAM_ENABLED:
        try:
            import mss
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                img = sct.grab(monitor)
                from PIL import Image
                pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
                pil_img.thumbnail((640, 360))

                buffer = io.BytesIO()
                pil_img.save(buffer, format="JPEG", quality=60)
                screen_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

                await api.send_screen(screen_data)
        except Exception as e:
            logger.debug(f"Screen stream error: {e}")

        await asyncio.sleep(STREAM_INTERVAL)


async def main():
    logger.info("=" * 50)
    logger.info("PRIME REMOTE D Agent starting...")
    logger.info(f"Device ID: {config.device_id}")
    logger.info(f"Device Name: {config.device_name}")
    logger.info(f"Backend: {config.backend_url}")
    logger.info("=" * 50)

    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return

    connected = False
    retry_count = 0
    max_retries = 10

    while not connected and retry_count < max_retries:
        try:
            logger.info("Connecting to backend...")
            connected = await api.health_check()
            if connected:
                logger.info("Connected to backend successfully!")
                await api.register()
            else:
                raise Exception("Health check failed")
        except Exception as e:
            retry_count += 1
            wait_time = min(2 ** retry_count, 60)
            logger.error(f"Connection failed: {e}. Retrying in {wait_time}s...")
            await asyncio.sleep(wait_time)

    if not connected:
        logger.error("Could not connect to backend after maximum retries.")
        return

    logger.info("Starting long polling + screen streaming...")
    asyncio.create_task(stream_screen())
    await start_polling()


def shutdown_handler(signum, frame):
    logger.info("Shutting down agent...")
    asyncio.get_event_loop().stop()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Agent stopped by user.")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        logger.info("Agent shutdown complete.")
