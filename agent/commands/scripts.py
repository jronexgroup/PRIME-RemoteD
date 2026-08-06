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
        for f in sorted(SCRIPTS_DIR.iterdir()):
            if f.suffix in (".bat", ".py", ".cmd", ".ps1"):
                scripts.append(f.name)
        if not scripts:
            return {"message": "No scripts found.\nPut .bat/.py files in agent/scripts/", "data": {"scripts": []}}
        script_list = "\n".join([f"📜 {s}" for s in scripts])
        return {"message": f"Available Scripts:\n{script_list}", "data": {"scripts": scripts}}
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
        if ext in (".bat", ".cmd"):
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
            error = result.stderr.strip()
            if error:
                output = f"ERROR:\n{error}"

        if not output:
            return {"message": f"✅ Script: {script_name}\n(Completed with no output)"}
        return {"message": f"✅ Script: {script_name}\n{output[:1500]}"}

    except subprocess.TimeoutExpired:
        return {"message": f"⏱ Script timed out (60s): {script_name}"}
    except Exception as e:
        logger.error(f"Run script failed: {e}")
        return {"message": f"❌ Failed: {str(e)}"}
