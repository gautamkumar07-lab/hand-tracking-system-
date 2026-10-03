"""Optional operating-system controls. Mouse control is opt-in."""
import platform

class SystemControls:
    def __init__(self):
        self.pyautogui = None
        self.mouse_enabled = False
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            self.pyautogui = pyautogui
        except Exception:
            pass

    def set_mouse_enabled(self, enabled: bool):
        self.mouse_enabled = bool(enabled and self.pyautogui is not None)
        return self.mouse_enabled

    def move_cursor(self, x_norm, y_norm):
        if not self.mouse_enabled or not self.pyautogui:
            return False
        try:
            sw, sh = self.pyautogui.size()
            x = max(0, min(sw - 1, int(x_norm * sw)))
            y = max(0, min(sh - 1, int(y_norm * sh)))
            self.pyautogui.moveTo(x, y, duration=0.02)
            return True
        except Exception:
            return False

    def click(self):
        if self.mouse_enabled and self.pyautogui:
            try:
                self.pyautogui.click()
                return True
            except Exception:
                pass
        return False

    def mouse_down(self):
        if self.mouse_enabled and self.pyautogui:
            try:
                self.pyautogui.mouseDown()
                return True
            except Exception:
                pass
        return False

    def mouse_up(self):
        if self.mouse_enabled and self.pyautogui:
            try:
                self.pyautogui.mouseUp()
                return True
            except Exception:
                pass
        return False

    def set_volume(self, level):
        """Set volume if a supported system backend is installed."""
        level = max(0, min(100, int(level)))
        if platform.system() == "Windows":
            try:
                from pycaw.pycaw import AudioUtilities
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import IAudioEndpointVolume
                device = AudioUtilities.GetSpeakers()
                interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level / 100, None)
                return True, f"Volume set to {level}%"
            except Exception:
                return False, "Install pycaw and comtypes on Windows to enable volume control."
        return False, "Volume control adapter is currently available only on Windows."

    def set_brightness(self, level):
        level = max(0, min(100, int(level)))
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return True, f"Brightness set to {level}%"
        except Exception:
            return False, "Brightness control is unsupported or unavailable on this device."
