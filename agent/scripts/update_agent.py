import subprocess
import os
import sys
import time

def run_update():
    agent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(agent_dir)

    print("[1/4] Stopping agent...")
    subprocess.run(["taskkill", "/IM", "pythonw.exe", "/F"], capture_output=True)
    subprocess.run(["taskkill", "/IM", "python.exe", "/F"], capture_output=True)
    time.sleep(2)

    print("[2/4] Pulling latest code...")
    result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("ERROR: git pull failed!")
        return False

    print("[3/4] Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"], capture_output=True)

    print("[4/4] Starting agent...")
    subprocess.Popen([sys.executable, "agent.py"], creationflags=0x08000000)

    print("\nUpdate complete! Agent restarted.")
    return True

if __name__ == "__main__":
    run_update()
