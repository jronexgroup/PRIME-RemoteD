import platform
import logging

logger = logging.getLogger("agent.system")


async def execute_system_info(cmd_type: str, args: dict) -> dict:
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        info = {
            "os": platform.system(),
            "os_version": platform.version(),
            "hostname": platform.node(),
            "cpu_percent": cpu_percent,
            "ram_total": f"{memory.total / (1024**3):.1f} GB",
            "ram_used": f"{memory.used / (1024**3):.1f} GB",
            "ram_percent": memory.percent,
            "disk_total": f"{disk.total / (1024**3):.1f} GB",
            "disk_used": f"{disk.used / (1024**3):.1f} GB",
            "disk_percent": disk.percent,
        }

        message = (
            f"System: {info['os']} {info['os_version']}\n"
            f"Host: {info['hostname']}\n"
            f"CPU: {info['cpu_percent']}%\n"
            f"RAM: {info['ram_used']}/{info['ram_total']} ({info['ram_percent']}%)\n"
            f"Disk: {info['disk_used']}/{info['disk_total']} ({info['disk_percent']}%)"
        )
        return {"message": message, "data": info}
    except ImportError:
        return {"message": "psutil not installed. Run: pip install psutil"}
    except Exception as e:
        logger.error(f"System info failed: {e}")
        return {"message": f"Failed: {str(e)}"}
