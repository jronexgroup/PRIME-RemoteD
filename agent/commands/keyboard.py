import logging

logger = logging.getLogger("agent.keyboard")

KEY_MAP = {
    "enter": "enter",
    "tab": "tab",
    "esc": "escape",
    "escape": "escape",
    "space": "space",
    "backspace": "backspace",
    "delete": "delete",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "home": "home",
    "end": "end",
    "pageup": "page_up",
    "pagedown": "page_down",
    "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
    "f5": "f5", "f6": "f6", "f7": "f7", "f8": "f8",
    "f9": "f9", "f10": "f10", "f11": "f11", "f12": "f12",
    "ctrl+c": "ctrl+c",
    "ctrl+v": "ctrl+v",
    "ctrl+x": "ctrl+x",
    "ctrl+z": "ctrl+z",
    "ctrl+a": "ctrl+a",
    "ctrl+s": "ctrl+s",
    "alt+tab": "alt+tab",
    "alt+f4": "alt+f4",
    "win": "win",
    "win+d": "win+d",
}


async def execute_keyboard(cmd_type: str, args: dict) -> dict:
    key = args.get("key", "").lower().strip()
    if not key:
        return {"message": "No key provided."}

    try:
        from pynput.keyboard import Key, Controller

        keyboard = Controller()

        if "+" in key:
            parts = key.split("+")
            keys_to_press = []
            for part in parts:
                part = part.strip()
                if part in ("ctrl", "control"):
                    keys_to_press.append(Key.ctrl_l)
                elif part == "alt":
                    keys_to_press.append(Key.alt_l)
                elif part in ("shift",):
                    keys_to_press.append(Key.shift_l)
                elif part in ("win", "cmd", "super"):
                    keys_to_press.append(Key.cmd)
                else:
                    keys_to_press.append(part)

            for k in keys_to_press:
                keyboard.press(k)
            for k in reversed(keys_to_press):
                keyboard.release(k)

            return {"message": f"Pressed: {key}"}

        mapped = KEY_MAP.get(key, key)
        if hasattr(Key, mapped):
            keyboard.press(getattr(Key, mapped))
            keyboard.release(getattr(Key, mapped))
        else:
            keyboard.press(key)
            keyboard.release(key)

        return {"message": f"Pressed: {key}"}

    except ImportError:
        return {"message": "pynput not installed. Run: pip install pynput"}
    except Exception as e:
        logger.error(f"Keyboard failed: {e}")
        return {"message": f"Keyboard failed: {str(e)}"}
