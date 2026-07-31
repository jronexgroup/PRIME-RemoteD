import platform
import subprocess
import logging

logger = logging.getLogger("agent.system")


async def execute_system_info(cmd_type: str, args: dict) -> dict:
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")

        hostname = platform.node()
        os_name = platform.system()
        os_version = platform.version()
        python_version = platform.python_version()

        uptime_seconds = psutil.boot_time()
        import time
        uptime = time.time() - uptime_seconds
        days = int(uptime // 86400)
        hours = int((uptime % 86400) // 3600)
        mins = int((uptime % 3600) // 60)

        message = (
            f"System Info\n"
            f"─────────────────\n"
            f"OS: {os_name} {os_version}\n"
            f"Host: {hostname}\n"
            f"Python: {python_version}\n"
            f"Uptime: {days}d {hours}h {mins}m\n"
            f"─────────────────\n"
            f"CPU: {cpu_percent}%\n"
            f"RAM: {memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB ({memory.percent}%)\n"
            f"Disk: {disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB ({disk.percent}%)\n"
        )
        return {"message": message}
    except ImportError:
        return {"message": "psutil not installed. Run: pip install psutil"}
    except Exception as e:
        logger.error(f"System info failed: {e}")
        return {"message": f"Failed: {str(e)}"}
