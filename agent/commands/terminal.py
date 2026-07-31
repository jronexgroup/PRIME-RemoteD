import subprocess
import logging

logger = logging.getLogger("agent.terminal")

ALLOWED_COMMANDS = [
    "dir", "ls", "cd", "echo", "type", "cls",
    "ipconfig", "ifconfig", "ping", "tracert", "nslookup",
    "systeminfo", "tasklist", "taskkill",
    "whoami", "hostname", "date", "time",
    "netstat", "net user", "net share",
    "findstr", "tree", "vol",
]


async def execute_terminal(cmd_type: str, args: dict) -> dict:
    command = args.get("command", "").strip()
    if not command:
        return {"message": "No command provided."}

    allowed = any(command.lower().startswith(cmd) for cmd in ALLOWED_COMMANDS)
    if not allowed:
        return {"message": f"Command not allowed: {command}\nAllowed: {', '.join(ALLOWED_COMMANDS[:10])}..."}

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            errors="replace"
        )

        output = result.stdout.strip()
        if result.returncode != 0 and not output:
            output = result.stderr.strip()

        if not output:
            return {"message": f"Command executed: {command}\n(No output)"}

        return {"message": f"$ {command}\n{output[:2000]}"}

    except subprocess.TimeoutExpired:
        return {"message": "Command timed out (30s)."}
    except Exception as e:
        logger.error(f"Terminal failed: {e}")
        return {"message": f"Failed: {str(e)}"}
