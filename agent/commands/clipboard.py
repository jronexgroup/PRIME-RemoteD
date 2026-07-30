import logging

logger = logging.getLogger("agent.clipboard")


async def execute_clipboard(cmd_type: str, args: dict) -> dict:
    try:
        import pyperclip

        if cmd_type == "clipboard_get":
            text = pyperclip.paste()
            if not text:
                return {"message": "Clipboard is empty."}
            return {"message": f"Clipboard:\n{text[:500]}"}

        elif cmd_type == "clipboard_set":
            text = args.get("text", "")
            if not text:
                return {"message": "No text provided."}
            pyperclip.copy(text)
            return {"message": "Text copied to clipboard."}

        return {"message": f"Unknown clipboard command: {cmd_type}"}

    except ImportError:
        return {"message": "pyperclip not installed. Run: pip install pyperclip"}
    except Exception as e:
        logger.error(f"Clipboard command failed: {e}")
        return {"message": f"Clipboard failed: {str(e)}"}
