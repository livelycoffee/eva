# ---------- IMPORTS ----------

import subprocess
import pyautogui
import shutil, os
import json
import screen_brightness_control as sbc
import pyvolume
from pathlib import Path

# ---------- APP REGISTRY SETUP ----------

file_path = Path(__file__)
src_path = file_path.parents[4]

WIN_APP_REG_FILE = src_path / f"assets/system/windows/windows_app_registry.json"
app_registry = {}

with open(WIN_APP_REG_FILE, "r") as file:
    app_registry = json.load(file)

# ---------- WINDOWS HELPER FUNCTIONS ----------

def get_app_cmd(target: str, intent: str) -> str:
    try:
        for app, data in app_registry.items():
            if target.lower() == app or target.lower() in data["aliases"]:
                if intent in data["cmd"]:
                    return data["cmd"][intent]
        return None
    except Exception as e:
        print([f"[ERR - receiving command]: {e}"])

# ---------- DEFAULT FUNCTION DEFINITIONS ----------


def open_app(target: str) -> bool:
    if not target:
        return False
    try: 
        intent = "open"
        cmd = get_app_cmd(target=target, intent=intent)
        # URI Schemes
        if cmd.startswith("http") or ":" in cmd:
            os.startfile(cmd)
        
        # Apps with flags
        elif " " in cmd:
            subprocess.Popen(["cmd", "/c", "start", "", *cmd.split()])
        
        else:
            exe = shutil.which(cmd)
            if exe:
                subprocess.Popen([exe])
            else:
                subprocess.Popen(["cmd", "/c", "start", "", cmd])
        return True

    except Exception as e:
        print(f"[ERR - open]: {e}")
        return False


def close_app(target: str) -> bool:
    if not target:
        return False
    try:
        intent = "close"
        cmd = get_app_cmd(intent=intent, target=target)
        subprocess.run(["taskkill", "/F", "/IM", cmd], check=True)
        return True
    
    except Exception as e:
        print(f"[ERR - taskkill]: {e}")
        return False


def take_screenshot(filename: str) -> bool:
    try:
        onedrive_path = os.environ.get("OneDrive")    
        if onedrive_path:
            folder_path = os.path.join(onedrive_path, "Pictures", "Screenshots")
        else:
            try:
                folder_path = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
    
            except:
                folder_path = "Screenshots"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

            full_path_name = os.path.join(folder_path, filename)
            pyautogui.screenshot(full_path_name)

            print(f"Captured. Saved as: {filename} to {folder_path}")
            return True

    except Exception as e:
        print(f"[ERR - screenshot]: {e}")
        return False


def get_battery_information() -> dict:
    raise NotImplementedError("[ERR]: Windows functionality has not been implemented!")


def open_file(path: str) -> bool:
    raise NotImplementedError("[ERR]: Windows functionality has not been implemented!")


def set_volume(level: int) -> bool:
    try:
        pyvolume.custom(percent = int(level))
        return True        
    
    except Exception as e:
        print(f"[ERR - volume]: {e}")
        return False

def set_brightness(level: int) -> bool:
    try:
        sbc.set_brightness(level)
        return True        
    
    except Exception as e:
        print(f"[ERR - brightness]: {e}")
        return False

# ---------- WINDOWS PLUGIN FUNCTIONS ----------

# >> For USER to Add Custom Windows Functions
# Make sure to add function counterpart in main_exec with proper docstrings.
# This is a place for windows specific functions, it is recommended to implement plugin functions in executor itself

#*---------- END OF CODE ----------*