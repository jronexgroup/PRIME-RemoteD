import subprocess
import logging

logger = logging.getLogger("agent.volume")

STARTUPINFO = subprocess.STARTUPINFO()
STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
STARTUPINFO.wShowWindow = 0


async def execute_volume(cmd_type: str, args: dict) -> dict:
    try:
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize

        CoInitialize()
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = interface.QueryInterface(IAudioEndpointVolume)

            if cmd_type == "volume_up":
                current = volume.GetMasterVolumeLevelScalar()
                new_vol = min(1.0, current + 0.1)
                volume.SetMasterVolumeLevelScalar(new_vol, None)
                return {"message": f"Volume: {int(new_vol * 100)}%"}

            elif cmd_type == "volume_down":
                current = volume.GetMasterVolumeLevelScalar()
                new_vol = max(0.0, current - 0.1)
                volume.SetMasterVolumeLevelScalar(new_vol, None)
                return {"message": f"Volume: {int(new_vol * 100)}%"}

            elif cmd_type == "volume_mute":
                volume.SetMute(1, None)
                return {"message": "Muted."}

            elif cmd_type == "volume_unmute":
                volume.SetMute(0, None)
                return {"message": "Unmuted."}
        finally:
            CoUninitialize()

    except Exception as e:
        logger.warning(f"pycaw failed, using fallback: {e}")
        try:
            if cmd_type == "volume_up":
                script = '$obj = New-Object -ComObject WScript.Shell; for($i=0;$i -lt 5;$i++){$obj.SendKeys([char]175)}'
                subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", script],
                             capture_output=True, timeout=10, startupinfo=STARTUPINFO, creationflags=0x08000000)
                return {"message": "Volume increased."}
            elif cmd_type == "volume_down":
                script = '$obj = New-Object -ComObject WScript.Shell; for($i=0;$i -lt 5;$i++){$obj.SendKeys([char]174)}'
                subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", script],
                             capture_output=True, timeout=10, startupinfo=STARTUPINFO, creationflags=0x08000000)
                return {"message": "Volume decreased."}
            elif cmd_type in ("volume_mute", "volume_unmute"):
                script = '$obj = New-Object -ComObject WScript.Shell; $obj.SendKeys([char]173)'
                subprocess.run(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", script],
                             capture_output=True, timeout=10, startupinfo=STARTUPINFO, creationflags=0x08000000)
                return {"message": "Toggled mute."}
        except Exception as e2:
            return {"message": f"Volume failed: {str(e2)}"}

    return {"message": f"Volume command completed."}
