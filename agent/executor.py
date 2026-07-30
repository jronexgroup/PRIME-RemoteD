import logging
from commands.power import execute_power
from commands.screen import execute_screenshot
from commands.system import execute_system_info

logger = logging.getLogger("agent.executor")

COMMAND_HANDLERS = {
    "shutdown": execute_power,
    "restart": execute_power,
    "sleep": execute_power,
    "lock": execute_power,
    "screenshot": execute_screenshot,
    "system_info": execute_system_info,
}


async def execute_command(cmd_type: str, args: dict) -> dict:
    handler = COMMAND_HANDLERS.get(cmd_type)
    if not handler:
        raise ValueError(f"Unsupported command: {cmd_type}")

    logger.info(f"Executing: {cmd_type} with args {args}")
    return await handler(cmd_type, args)
