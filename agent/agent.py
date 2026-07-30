import asyncio
import sys
import signal
from logger import setup_logger
from config import config
from api import api
from polling import start_polling

logger = setup_logger()


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

    logger.info("Starting long polling...")
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
