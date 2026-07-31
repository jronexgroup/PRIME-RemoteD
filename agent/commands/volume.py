import logging

logger = logging.getLogger("agent.volume")


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
                current_mute = volume.GetMute()
                volume.SetMute(1, None)
                return {"message": "Muted."}

            elif cmd_type == "volume_unmute":
                volume.SetMute(0, None)
                return {"message": "Unmuted."}

            return {"message": f"Unknown volume command: {cmd_type}"}
        finally:
            CoUninitialize()

    except ImportError:
        return {"message": "pycaw not installed. Run: pip install pycaw comtypes"}
    except Exception as e:
        logger.error(f"Volume command failed: {e}")
        return {"message": f"Volume failed: {str(e)}"}
