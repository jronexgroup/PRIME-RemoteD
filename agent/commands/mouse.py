import logging

logger = logging.getLogger("agent.mouse")

SAVED_COORDS = {
    "browser_back": {"x": 24, "y": 69, "name": "🔙 Back"},
    "browser_forward": {"x": 64, "y": 69, "name": "🔜 Forward"},
    "browser_refresh": {"x": 109, "y": 69, "name": "🔄 Refresh"},
    "browser_address": {"x": 650, "y": 69, "name": "📍 Address Bar"},
    "browser_bookmark": {"x": 1316, "y": 69, "name": "⭐ Bookmark"},
    "browser_new_tab": {"x": 328, "y": 24, "name": "➕ New Tab"},
    "browser_close_tab": {"x": 289, "y": 24, "name": "❌ Close Tab"},
    "browser_minimize": {"x": 1410, "y": 24, "name": "➖ Minimize"},
    "browser_maximize": {"x": 1460, "y": 24, "name": "⬜ Maximize"},
    "browser_close": {"x": 1510, "y": 24, "name": "❌ Close Window"},
    "browser_menu": {"x": 1510, "y": 69, "name": "⋮ Chrome Menu"},
    "browser_profile": {"x": 1485, "y": 167, "name": "👤 Profile"},
    "youtube_search": {"x": 720, "y": 170, "name": "🔍 YouTube Search"},
    "youtube_search_btn": {"x": 1078, "y": 170, "name": "🔎 Search Button"},
    "youtube_menu": {"x": 42, "y": 169, "name": "☰ YouTube Menu"},
}


async def execute_mouse(cmd_type: str, args: dict) -> dict:
    try:
        from pynput.mouse import Controller, Button
        import time

        mouse = Controller()

        if cmd_type == "mouse_move":
            x = int(args.get("x", 0))
            y = int(args.get("y", 0))
            mouse.position = (x, y)
            return {"message": f"Mouse moved to ({x}, {y})"}

        elif cmd_type == "mouse_click":
            x = int(args.get("x", 0))
            y = int(args.get("y", 0))
            mouse.position = (x, y)
            button = args.get("button", "left")
            if button == "right":
                mouse.click(Button.right)
            elif button == "middle":
                mouse.click(Button.middle)
            else:
                mouse.click(Button.left)
            return {"message": f"Clicked ({x}, {y})"}

        elif cmd_type == "mouse_double_click":
            x = int(args.get("x", 0))
            y = int(args.get("y", 0))
            mouse.position = (x, y)
            mouse.click(Button.left, 2)
            return {"message": f"Double-clicked ({x}, {y})"}

        elif cmd_type == "mouse_scroll":
            dx = int(args.get("dx", 0))
            dy = int(args.get("dy", 0))
            mouse.scroll(dx, dy)
            return {"message": f"Scrolled ({dx}, {dy})"}

        elif cmd_type == "mouse_click_sequence":
            coords = args.get("coords", [])
            if not coords:
                return {"message": "No coordinates provided."}

            for i, coord in enumerate(coords):
                x, y = int(coord["x"]), int(coord["y"])
                mouse.position = (x, y)
                mouse.click(Button.left)
                time.sleep(0.3)

            return {"message": f"Executed {len(coords)} clicks."}

        elif cmd_type == "mouse_preset":
            preset = args.get("preset", "")
            if preset in SAVED_COORDS:
                point = SAVED_COORDS[preset]
                mouse.position = (point["x"], point["y"])
                mouse.click(Button.left)
                return {"message": f"Clicked: {point['name']} ({point['x']}, {point['y']})"}
            return {"message": f"Unknown preset: {preset}"}

        return {"message": f"Unknown mouse command: {cmd_type}"}

    except ImportError:
        return {"message": "pynput not installed. Run: pip install pynput"}
    except Exception as e:
        logger.error(f"Mouse failed: {e}")
        return {"message": f"Mouse failed: {str(e)}"}
