# ---------- IMPORTS ----------

import datetime
import webbrowser
import urllib.parse
import requests
import bs4
import wikipedia
import time

import platform
from _platform import macos, windows
from int_check import is_connected

# ---------- PLATFORM AND HASHMAP SETUP ----------

command_registry = {}

def register(name):
    def decorator(func):
        command_registry[name] = func
        return func
    return decorator

_platform = {
    "Darwin": macos,
    "Windows": windows
}

PLATFORM = platform.system()

# DEVELOPER NOTE #----------------------------------------------------------------------------------
# Most of these functions were created keeping in mind macOS (Apple Sillicon) functionality in mind.
# Windows-Compatible Versions (and maybe even a Linux compatible version) will be coming out soon.
#---------------------------------------------------------------------------------------------------

# ---------- HELPER FUNCTION DEFINITIONS ----------

# Add as required.

# ---------- DEFAULT FUNCTION DEFINITIONS ---------- (PLATFORM SPECIFIC)

@register("open_app")
def open_app(target: str) -> bool:
    '''
    Opens applications on the user device.

    Args:
        target (str): Name of app you want to OPEN.

    Returns:
        bool: Success status of opening the app.
    '''
    return _platform[PLATFORM].open_app(target)


@register("close_app")
def close_app(target: str) -> bool:
    '''
    Closes applications on the user device.

    Args:
        target (str): Name of app you want to CLOSE.

    Returns:
        bool: Success status of closing the app.
    '''
    return _platform[PLATFORM].close_app(target)


@register("take_screenshot")
def take_screenshot(filename: str) -> bool:
    '''
    Function to take a screenshot.

    Args:
        filename (str): Name of the file (or path) you want to save the screenshot as.

    Returns:
        status (bool): Status of taking a screenshot.
    '''
    return _platform[PLATFORM].take_screenshot(filename)


@register("get_battery_information")
def get_battery_information() -> dict:
    '''
    Function to get power/battery levels/information of the user device.

    Returns:
        battery_information (dict): Various information regarding the device battery level.
    '''
    return _platform[PLATFORM].get_battery_information()


@register("open_file")
def open_file(path: str) -> bool:
    """
    Open a file or folder.

    Args:
        path (str): Path to file or folder. (use local path r\"Screenshots/<filename>\" for Screenshots)

    Returns:
        status (bool): Success status of opening the file.
    """
    return _platform[PLATFORM].open_file(path)


@register("set_volume")
def set_volume(level: int) -> bool:
    """
    Set system volume.

    Args:
        level (int): Volume level (0-100)

    Returns:
        status (bool): Success status of changing the volume.
    """
    return _platform[PLATFORM].set_volume(level)


@register("set_brightness")
def set_brightness(level: int) -> bool:
    '''
    Function to set the brightness of user device display to certain level (eg. 20%).

    Args:
        level (int): The brightness level to set display at.

    Returns:
        status (bool): Success status of setting the brightness.
    '''
    return _platform[PLATFORM].set_brightness(level)


@register("get_current_app")
def get_current_app() -> str:
    '''
    Function to get the name of the currently active app on the user's screen.

    Returns:
        app_name (str): Name of current active app.
    '''
    return _platform[PLATFORM].get_current_app()


# ---------- DEFAULT FUNCTION DEFINITIONS ---------- (PLATFORM INDEPENDENT)

@register("get_current_time")
def get_current_time() -> str:
    '''
    Function to get the current time.

    Returns:
        time (str): Current time.
    '''
    time = datetime.datetime.now().strftime("%-I:%M %p")
    return str(time)


@register("get_current_date")
def get_current_date() -> str:
    '''
    Function to get the current date.

    Returns:
        date (str): Today's Date.
    '''
    date = datetime.date.today()
    return str(date)


@register("get_current_day")
def get_current_day() -> str:
    '''
    Function to get today's day. (eg. Sunday, Monday)

    Returns:
        day (str): Today's Day
    '''
    day = datetime.datetime.now().strftime("%A")
    return str(day)


@register("open_link") # --> PLATFORM INDEPENDENT
def open_link(url: str) -> bool:
    '''
    Function to open a link in the browser or open web apps in the browser.

    Args:
        url (str): link the user wants to search for. (eg. youtube.com)
    
    Returns:
        status (bool): Success status of opening link.
    '''
    if not url:
        return False
    try:
        target = url.strip()
        if not target.startswith(("http://", "https://")):
            target = "https://" + target
        webbrowser.open(target, new=2)
        return True
    except Exception as e:
        print(f"[ERR - open_link]: {e}")
        return False


@register("search_youtube") # --> PLATFORM INDEPENDENT
def search_youtube(query: str) -> bool:
    '''
    Function to search on YouTube.

    Args:
        query (str): String to search on youtube for.

    Returns:
        status (bool): Success status of searching on YouTube.
    '''
    if not query:
        return False
    try:
        encoded = urllib.parse.quote(query.strip())
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f"[ERR - search_yt]: {e}")
        return False


@register("search_web") # --> PLATFORM INDEPENDENT
def search_web(query: str) -> bool:
    '''
    Function to search for a general query on the browser.

    Args:
        query (str): What the user wants to search for. (eg. How to bake a cake?)

    Returns:
        status (bool): Success status of searching the web.
    '''
    if not query:
        return False
    try:
        encoded = urllib.parse.quote(query.strip())
        url = f"https://duckduckgo.com/?q={encoded}"
        webbrowser.open(url, new=2)
        return True
    except Exception as e:
        print(f"[ERR - search_web]: {e}")
        return False
    

@register("search_wikipedia")
def search_wikipedia(query: str) -> str:
    '''
    Function to search wikipedia and get a summary for the given topic title.

    Args:
        query (str): Topic title to get summary from wikipedia for.

    Return:
        result (str): Summary of given topic title.
    '''
    try:
        query = wikipedia.search(str(query))[0]
        return wikipedia.summary(str(query), sentences=2, auto_suggest=False)
    except Exception as e:
        print(f"[ERR - search_wikipedia]: {e}")
        return "Could not search wikipedia!"


@register("play_on_youtube")
def play_on_youtube(query: str) -> str:
    '''
    Function to directly play the first result of a query on YouTube.
    Used to directly play YouTube videos.

    Args:
        query (str): The query to search for and play the first result of.
    
    Returns:
        status (str): Result of playing the YouTube video.
    '''
    encoded = urllib.parse.quote(query.strip())
    url = f"https://www.youtube.com/results?search_query={encoded}"
    try:
        web_page = requests.get(url, timeout=5)
        data = web_page.content
        data = str(data)
        elements = data.split('"')

        for element in elements:
            if element == "WEB_PAGE_TYPE_WATCH":
                index = elements.index(element) + 1
                break
        
        completor = elements[index-5]
        if completor == "/results":
            print(f"[ERR - play_on_youtube]: No video found for this query!")
            return "No YouTube video found for this query"

        video = f"https://www.youtube.com{completor}"
        webbrowser.open(video, new=2)

        video_page = requests.get(video, timeout=5)
        html = bs4.BeautifulSoup(video_page.text, features="html.parser")
        return f"Playing {str(html.title.string)}..."
    
    except Exception as e:
        print(f"[ERR - play_on_youtube]: {e}")
        return "Could not play YouTube video!"


# ---------- DEFAULT FUNCTION DEFINITIONS ---------- (Pythonic)

@register("wait_function") # --> Pythonic Function
def wait_function(seconds: int) -> None:
    '''
    Function to wait for the given amount of time in seconds.

    Args:
        seconds (int): The number of seconds you want to wait for.

    Returns:
        None
    '''
    time.sleep(seconds)


@register("check_internet") # --> PLATFORM INDEPENDENT
def check_internet() -> bool:
    """
    Check if the device is connected to the internet.

    Returns:
        status (bool): Status of Internet Connection.
    """
    return is_connected()


# @register("shutdown") # --> Pythonic Function
# def shutdown() -> None:
#     '''
#     Function to exit the program and shutdown EVA. (IF user says goodbye or asks to exit/shutdown).
#
#     Returns:
#         None
#     '''
#     exit()


# ---------- PLUGIN FUNCTION DEFINITIONS ---------- --> TEMP

# >> For USER to Add Custom Functions
# Make sure to provide proper docstrings to each function. --> Helps LLM with tool-calling


# ---------- MAIN EXEC REQUESTOR ----------

def request_exec(query):
    try:
        intent = query["intent"]
        kwargs = query["parameters"]
        if intent in command_registry:
            command_registry[intent](**kwargs)
            return True
        else:
            return False
    except:
        return False

#*---------- END OF CODE ----------*