import platform
import subprocess
import time
import logging

logger = logging.getLogger("agent.system")


async def execute_system_info(cmd_type: str, args: dict) -> dict:
    try:
        hostname = platform.node()
        os_name = platform.system()
        os_version = platform.version()
        python_version = platform.python_version()
        processor = platform.processor()

        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            mins = int((uptime_seconds % 3600) // 60)

            message = (
                f"System Info\n"
                f"─────────────────\n"
                f"OS: {os_name} {os_version}\n"
                f"Host: {hostname}\n"
                f"CPU: {processor}\n"
                f"CPU Usage: {cpu_percent}%\n"
                f"RAM: {memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB ({memory.percent}%)\n"
                f"Disk C: {disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB ({disk.percent}%)\n"
                f"Uptime: {days}d {hours}h {mins}m\n"
                f"Python: {python_version}"
            )
        except ImportError:
            message = (
                f"System Info\n"
                f"─────────────────\n"
                f"OS: {os_name} {os_version}\n"
                f"Host: {hostname}\n"
                f"CPU: {processor}\n"
                f"Python: {python_version}\n"
                f"─────────────────\n"
                f"(Install psutil for RAM/Disk/CPU details)"
            )

        return {"message": message}
    except Exception as e:
        logger.error(f"System info failed: {e}")
        return {"message": f"Failed: {str(e)}"}
