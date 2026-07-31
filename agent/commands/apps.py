import subprocess
import webbrowser
import logging

logger = logging.getLogger("agent.apps")


async def execute_open_url(cmd_type: str, args: dict) -> dict:
    url = args.get("url", "")
    if not url:
        return {"message": "No URL provided."}
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        webbrowser.open(url)
        return {"message": f"Opened: {url}"}
    except Exception as e:
        logger.error(f"Open URL failed: {e}")
        return {"message": f"Failed: {str(e)}"}


async def execute_open_app(cmd_type: str, args: dict) -> dict:
    app = args.get("app", "")
    if not app:
        return {"message": "No app name provided."}
    try:
        subprocess.Popen(f"start {app}", shell=True)
        return {"message": f"Opened: {app}"}
    except Exception as e:
        logger.error(f"Open app failed: {e}")
        return {"message": f"Failed: {str(e)}"}
