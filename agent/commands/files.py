import os
import logging
from pathlib import Path

logger = logging.getLogger("agent.files")


async def execute_list_dir(cmd_type: str, args: dict) -> dict:
    path = args.get("path", "C:\\")
    try:
        p = Path(path)
        if not p.exists():
            return {"message": f"Path not found: {path}"}
        if not p.is_dir():
            return {"message": f"Not a directory: {path}"}

        items = []
        for item in sorted(p.iterdir()):
            try:
                if item.is_dir():
                    items.append({"name": item.name, "type": "folder", "size": 0})
                else:
                    size = item.stat().st_size
                    items.append({"name": item.name, "type": "file", "size": size})
            except PermissionError:
                items.append({"name": item.name, "type": "locked", "size": 0})

        folders = [i for i in items if i["type"] == "folder"]
        files = [i for i in items if i["type"] in ("file", "locked")]

        message = f"📂 {path}\n"
        message += f"─────────────────\n"
        if folders:
            message += f"Folders: {len(folders)}\n"
        if files:
            message += f"Files: {len(files)}\n"
        message += f"Total: {len(items)} items"

        return {"message": message, "data": {"path": str(p), "items": items[:50]}}

    except Exception as e:
        logger.error(f"List dir failed: {e}")
        return {"message": f"Failed: {str(e)}"}


async def execute_file_info(cmd_type: str, args: dict) -> dict:
    path = args.get("path", "")
    if not path:
        return {"message": "No path provided."}

    try:
        p = Path(path)
        if not p.exists():
            return {"message": f"File not found: {path}"}

        stat = p.stat()
        size = stat.st_size
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size // 1024} KB"
        else:
            size_str = f"{size // (1024 * 1024)} MB"

        return {
            "message": f"📄 {p.name}\nSize: {size_str}\nPath: {p}",
            "data": {"path": str(p), "size": size}
        }
    except Exception as e:
        return {"message": f"Failed: {str(e)}"}
