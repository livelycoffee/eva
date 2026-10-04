# ---------- IMPORTS ----------

import subprocess, os
import json
import re

# ---------- APP REGISTRY SETUP ----------

MACOS_APP_REG_FILE = f"assets/system/macos/macos_app_registry.json"
app_registry = {}

with open(MACOS_APP_REG_FILE, "r") as file:
    app_registry = json.load(file)

# ---------- MACOS HELPER FUNCTIONS ----------

def get_active_app():
    script = 'tell application "System Events" to get name of first application process whose frontmost is true'
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def find_app(name: str):
    try:
        result = subprocess.run(
            [
                "mdfind",
                f"kMDItemKind == 'Application' && kMDItemDisplayName == '*{name}*'"
            ],
            capture_output=True,
            text=True)
        apps = result.stdout.strip().split("\n")
        if apps and apps[0]:
            return os.path.basename(apps[0]).replace(".app", "")
        return None
    except Exception as e:
        print("Search error:", e)
        return None

def get_app(target: str):
    for app, data in app_registry.items():
        if target.lower() == app or target.lower() in data["aliases"]:
            if data["name"] == "current_app":
                return get_active_app()
            return str(data["name"])
    found = find_app(target)
    if found:
        return found
    return target

# ---------- DEFAULT FUNCTION DEFINITIONS ----------

def open_app(target: str) -> bool:
    if not target:
        return False
    try:
        target = get_app(target=target)
        subprocess.run(["open", "-a", target], check=True)
        return True
    except Exception as e:
        print(f"[ERR - open_app]: {e}")
        return False


def close_app(target: str) -> bool:
    if not target:
        return False
    try:
        target = get_app(target=target)
        applescript = f'tell application "{target}" to quit'
        subprocess.run(["osascript", "-e", applescript], check=True)
        #os.system(f"osascript -e '{applescript}'") -> soft depriciated
        return True
    except Exception as e:
        print(f"[ERR - close_app]: {e}")
        return False


def take_screenshot(filename: str) -> bool:
    filepath = os.path.join("Screenshots", filename)
    try:
        subprocess.run(["screencapture", filepath], check=True) 
        return True
    except:
        return False


def get_battery_information() -> dict:
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True
        )
        match = re.search(r'(\d+)%;\s*(\w+);\s*([\d:]+ remaining|no estimate)', result.stdout)
        if not match:
            return None
        percentage = int(match.group(1))
        charging_status = match.group(2).lower()
        time_remaining = match.group(3)
        return {
            "percentage": percentage,
            "status": charging_status,
            "time_remaining": time_remaining
        }
    except Exception as e:
        print(f"[ERR - battery]: {e}")
        return None


def open_file(path: str) -> bool:
    if not path:
        return False
    try:
        subprocess.run(["open", path], check=True)
        return True
    except Exception as e:
        print(f"[ERR - open_file]: {e}")
        return False


def set_volume(level: int) -> bool:
    try:
        level = int(level)
        level = max(0, min(100, level))
        subprocess.run([
            "osascript",
            "-e",
            f"set volume output volume {level}"
        ], check=True)
        return True
    except Exception as e:
        print(f"[ERR - set_vol]: {e}")
        return False
    

def set_brightness(level: int) -> bool:
    try:
        level = int(level)
        level = max(0, min(100, level))
        level = float(level)/100
        subprocess.run(["brightness", str(level)], check=True)
        return True
    except Exception as e:
        print(f"[ERR - set_brightness]: {e}")
        return False


def get_current_app() -> str:
    return get_active_app()

# ---------- MACOS PLUGIN FUNCTIONS ----------

# >> For USER to Add Custom macOS (Darwin) Functions
# Make sure to add function counterpart in main_exec with proper docstrings.
# This is a place for macos specific functions, it is recommended to implement plugin functions in executor itself

#*---------- END OF CODE ----------*