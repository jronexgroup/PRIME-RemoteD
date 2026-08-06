import subprocess
import os
import tempfile
import logging

logger = logging.getLogger("agent.show")

STARTUPINFO = subprocess.STARTUPINFO()
STARTUPINFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
STARTUPINFO.wShowWindow = 0


async def execute_show_text(cmd_type: str, args: dict) -> dict:
    text = args.get("text", "")
    if not text:
        return {"message": "No text provided."}

    try:
        html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>
body {{
    margin: 0;
    padding: 0;
    background: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-family: Arial, sans-serif;
}}
.text {{
    text-align: center;
    padding: 40px;
    word-wrap: break-word;
    max-width: 90vw;
}}
</style>
</head>
<body>
<div class="text" id="text"></div>
<script>
var text = {repr(text)};
var len = text.length;
var fontSize;
if (len < 20) fontSize = 120;
else if (len < 50) fontSize = 80;
else if (len < 100) fontSize = 60;
else if (len < 200) fontSize = 48;
else if (len < 500) fontSize = 36;
else fontSize = 28;
document.getElementById('text').style.fontSize = fontSize + 'px';
document.getElementById('text').innerText = text;
</script>
</body>
</html>"""

        temp_dir = tempfile.gettempdir()
        html_path = os.path.join(temp_dir, "show_text.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        subprocess.Popen(
            ["cmd", "/c", "start", "", html_path],
            startupinfo=STARTUPINFO,
            creationflags=0x08000000
        )

        return {"message": f"✅ Displaying text on screen.\nClose the window to dismiss."}

    except Exception as e:
        logger.error(f"Show text failed: {e}")
        return {"message": f"❌ Failed: {str(e)}"}


async def execute_play_audio(cmd_type: str, args: dict) -> dict:
    audio_path = args.get("audio_path", "")
    if not audio_path:
        return {"message": "No audio file provided."}

    try:
        if not os.path.exists(audio_path):
            return {"message": f"Audio file not found: {audio_path}"}

        subprocess.Popen(
            ["cmd", "/c", "start", "", audio_path],
            startupinfo=STARTUPINFO,
            creationflags=0x08000000
        )

        return {"message": f"🎵 Playing audio: {os.path.basename(audio_path)}"}

    except Exception as e:
        logger.error(f"Play audio failed: {e}")
        return {"message": f"❌ Failed: {str(e)}"}
