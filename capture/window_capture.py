import pygetwindow as gw
import pyautogui
from PIL import Image

def capture_window(title):
    """특정 창 캡쳐"""
    try:
        window = gw.getWindowsWithTitle(title)[0]
        if window:
            window.activate()
            window.moveTo(0, 0)
            window.resizeTo(1920, 1080)
            pyautogui.screenshot('window_screenshot.png', region=(window.left, window.top, window.width, window.height))
            return Image.open('window_screenshot.png')
    except Exception as e:
        print(f"Error capturing window: {e}")
        return None