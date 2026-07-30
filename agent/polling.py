import asyncio
import logging
from api import api
from executor import execute_command
from config import config

logger = logging.getLogger("agent.polling")
BACKOFF_BASE = 2
BACKOFF_MAX = 60


async def start_polling():
    logger.info("Starting long polling...")
    backoff = BACKOFF_BASE

    while True:
        try:
            commands = await api.poll_commands(timeout=30)
            if commands:
                backoff = BACKOFF_BASE
                for cmd in commands:
                    logger.info(f"Received command: {cmd.get('id')} ({cmd.get('type')})")
                    asyncio.create_task(process_command(cmd))
            else:
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            await asyncio.sleep(min(backoff, BACKOFF_MAX))
            backoff *= 2


async def process_command(cmd: dict):
    cmd_id = cmd.get("id", "unknown")
    cmd_type = cmd.get("type", "unknown")
    cmd_args = cmd.get("args", {})

    try:
        result = await execute_command(cmd_type, cmd_args)
        await api.send_result(cmd_id, "success", result.get("message", "Done"), result.get("data", {}))
        logger.info(f"Command {cmd_id} completed successfully")
    except Exception as e:
        await api.send_result(cmd_id, "error", str(e))
        logger.error(f"Command {cmd_id} failed: {e}")
