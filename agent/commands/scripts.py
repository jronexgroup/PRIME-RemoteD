import subprocess
import os
import logging
from pathlib import Path

logger = logging.getLogger("agent.scripts")

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


async def execute_list_scripts(cmd_type: str, args: dict) -> dict:
    try:
        SCRIPTS_DIR.mkdir(exist_ok=True)
        scripts = []
        for f in SCRIPTS_DIR.iterdir():
            if f.suffix in (".bat", ".py", ".cmd", ".ps1"):
                scripts.append(f.name)
        if not scripts:
            return {"message": "No scripts found in scripts/ folder.", "data": {"scripts": []}}
        return {"message": f"Found {len(scripts)} scripts.", "data": {"scripts": scripts}}
    except Exception as e:
        logger.error(f"List scripts failed: {e}")
        return {"message": f"Failed: {str(e)}"}


async def execute_run_script(cmd_type: str, args: dict) -> dict:
    script_name = args.get("script", "")
    if not script_name:
        return {"message": "No script name provided."}

    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {"message": f"Script not found: {script_name}"}

    try:
        ext = script_path.suffix.lower()
        if ext == ".bat" or ext == ".cmd":
            result = subprocess.run(
                ["cmd", "/c", str(script_path)],
                capture_output=True, text=True, timeout=60
            )
        elif ext == ".py":
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True, text=True, timeout=60
            )
        elif ext == ".ps1":
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
                capture_output=True, text=True, timeout=60
            )
        else:
            return {"message": f"Unsupported script type: {ext}"}

        output = result.stdout.strip()
        if result.returncode != 0:
            output = result.stderr.strip() or output

        if not output:
            return {"message": f"Script executed: {script_name}\n(No output)"}
        return {"message": f"Script: {script_name}\n{output[:1000]}"}

    except subprocess.TimeoutExpired:
        return {"message": "Script timed out (60s limit)."}
    except Exception as e:
        logger.error(f"Run script failed: {e}")
        return {"message": f"Failed: {str(e)}"}
