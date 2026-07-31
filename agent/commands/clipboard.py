import subprocess
import logging

logger = logging.getLogger("agent.clipboard")


async def execute_clipboard(cmd_type: str, args: dict) -> dict:
    try:
        if cmd_type == "clipboard_get":
            script = "Get-Clipboard -Format Text -Raw"
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                capture_output=True, text=True, timeout=15
            )
            text = result.stdout.strip()
            if not text:
                return {"message": "Clipboard is empty."}
            return {"message": f"Clipboard:\n{text[:1000]}"}

        elif cmd_type == "clipboard_set":
            text = args.get("text", "")
            if not text:
                return {"message": "No text provided."}
            script = f'Set-Clipboard -Value "{text}"'
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                capture_output=True, text=True, timeout=15
            )
            return {"message": "Text copied to clipboard."}

        return {"message": f"Unknown clipboard command: {cmd_type}"}

    except subprocess.TimeoutExpired:
        return {"message": "Clipboard command timed out."}
    except Exception as e:
        logger.error(f"Clipboard command failed: {e}")
        return {"message": f"Clipboard failed: {str(e)}"}
