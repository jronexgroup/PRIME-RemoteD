import subprocess
import logging

logger = logging.getLogger("agent.clipboard")


async def execute_clipboard(cmd_type: str, args: dict) -> dict:
    try:
        if cmd_type == "clipboard_get":
            result = subprocess.run(
                ["powershell", "-command", "Get-Clipboard"],
                capture_output=True, text=True, timeout=10
            )
            text = result.stdout.strip()
            if not text:
                return {"message": "Clipboard is empty."}
            return {"message": f"Clipboard:\n{text[:500]}"}

        elif cmd_type == "clipboard_set":
            text = args.get("text", "")
            if not text:
                return {"message": "No text provided."}
            subprocess.run(
                ["powershell", "-command", f"Set-Clipboard -Value '{text}'"],
                capture_output=True, timeout=10
            )
            return {"message": "Text copied to clipboard."}

        return {"message": f"Unknown clipboard command: {cmd_type}"}

    except Exception as e:
        logger.error(f"Clipboard command failed: {e}")
        return {"message": f"Clipboard failed: {str(e)}"}
