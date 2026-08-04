import time
import logging

logger = logging.getLogger("agent.mouse")


async def execute_mouse(cmd_type: str, args: dict) -> dict:
    try:
        from pynput.mouse import Controller, Button

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
                logger.info(f"Click {i+1}/{len(coords)} at ({x}, {y})")

            return {"message": f"Executed {len(coords)} clicks."}

        return {"message": f"Unknown mouse command: {cmd_type}"}

    except ImportError:
        return {"message": "pynput not installed. Run: pip install pynput"}
    except Exception as e:
        logger.error(f"Mouse failed: {e}")
        return {"message": f"Mouse failed: {str(e)}"}
