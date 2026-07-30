import subprocess
import logging

logger = logging.getLogger("agent.power")

POWER_COMMANDS = {
    "shutdown": "shutdown /s /t 0",
    "restart": "shutdown /r /t 0",
    "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0",
    "lock": "rundll32.exe user32.dll,LockWorkStation",
}


async def execute_power(cmd_type: str, args: dict) -> dict:
    command = POWER_COMMANDS.get(cmd_type)
    if not command:
        return {"message": f"Unknown power command: {cmd_type}"}

    try:
        subprocess.run(command, shell=True, check=False)
        messages = {
            "shutdown": "Shutdown initiated.",
            "restart": "Restart initiated.",
            "sleep": "Sleep mode activated.",
            "lock": "Workstation locked.",
        }
        return {"message": messages.get(cmd_type, "Power command executed.")}
    except Exception as e:
        logger.error(f"Power command failed: {e}")
        return {"message": f"Failed: {str(e)}"}
