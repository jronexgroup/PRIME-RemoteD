import subprocess
import logging

logger = logging.getLogger("agent.volume")


async def execute_volume(cmd_type: str, args: dict) -> dict:
    try:
        if cmd_type == "volume_up":
            script = '''
            $wsh = New-Object -ComObject WScript.Shell
            for ($i=0; $i -lt 5; $i++) {
                $wsh.SendKeys([char]175)
            }
            '''
            subprocess.run(["powershell", "-command", script], capture_output=True, timeout=10)
            return {"message": "Volume increased."}

        elif cmd_type == "volume_down":
            script = '''
            $wsh = New-Object -ComObject WScript.Shell
            for ($i=0; $i -lt 5; $i++) {
                $wsh.SendKeys([char]174)
            }
            '''
            subprocess.run(["powershell", "-command", script], capture_output=True, timeout=10)
            return {"message": "Volume decreased."}

        elif cmd_type == "volume_mute":
            subprocess.run(["powershell", "-command", "New-Object -ComObject WScript.Shell.SendKeys([char]173)"], capture_output=True, timeout=10)
            return {"message": "Muted/Unmuted."}

        elif cmd_type == "volume_unmute":
            subprocess.run(["powershell", "-command", "New-Object -ComObject WScript.Shell.SendKeys([char]173)"], capture_output=True, timeout=10)
            return {"message": "Muted/Unmuted."}

        return {"message": f"Unknown volume command: {cmd_type}"}

    except Exception as e:
        logger.error(f"Volume command failed: {e}")
        return {"message": f"Volume failed: {str(e)}"}
