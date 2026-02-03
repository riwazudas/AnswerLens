"""
Screen Analysis Application
Captures screen content and uses LLM to analyze and answer questions
"""

import mss
import mss.tools
from PIL import Image
import io
import base64
from datetime import datetime
import os
import sys

# Windows-specific imports
if sys.platform == 'win32':
    import win32gui
    import win32ui
    import win32con
    from ctypes import windll


class ScreenCapture:
    """Handles screen capturing functionality"""
    
    def __init__(self):
        self.sct = mss.mss()
    
    def capture_screen(self, monitor_number=1):
        """
        Capture the specified monitor screen
        
        Args:
            monitor_number: Monitor to capture (1 for primary, 0 for all)
        
        Returns:
            PIL Image object
        """
        monitor = self.sct.monitors[monitor_number]
        screenshot = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img
    
    def capture_region(self, left, top, width, height):
        """
        Capture a specific region of the screen
        
        Args:
            left, top: Top-left corner coordinates
            width, height: Region dimensions
        
        Returns:
            PIL Image object
        """
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
        screenshot = self.sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        return img
    
    def save_screenshot(self, img, filename=None):
        """Save screenshot to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        img.save(filename)
        return filename
    
    def image_to_base64(self, img, format='PNG', max_size=1024):
        """
        Convert PIL Image to base64 string, with optional resizing
        
        Args:
            img: PIL Image object
            format: Image format (PNG, JPEG)
            max_size: Maximum dimension (width or height) for resizing
        
        Returns:
            Base64 encoded string
        """
        # Resize if image is too large
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffered = io.BytesIO()
        img.save(buffered, format=format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def list_windows(self):
        """
        List all visible windows (Windows only)
        
        Returns:
            List of tuples (window_handle, window_title)
        """
        if sys.platform != 'win32':
            raise NotImplementedError("Window listing is only supported on Windows")
        
        windows = []
        
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Only include windows with titles
                    windows.append((hwnd, title))
            return True
        
        win32gui.EnumWindows(callback, None)
        return windows
    
    def capture_window(self, window_handle):
        """
        Capture a specific window by its handle (Windows only)
        
        Args:
            window_handle: Window handle (HWND)
        
        Returns:
            PIL Image object
        """
        if sys.platform != 'win32':
            raise NotImplementedError("Window capture is only supported on Windows")
        
        try:
            # Get window dimensions
            left, top, right, bottom = win32gui.GetWindowRect(window_handle)
            width = right - left
            height = bottom - top
            
            # Get window device context
            hwnd_dc = win32gui.GetWindowDC(window_handle)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            
            # Create bitmap
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(bitmap)
            
            # Copy window content
            windll.user32.PrintWindow(window_handle, save_dc.GetSafeHdc(), 3)
            
            # Convert to PIL Image
            bmpinfo = bitmap.GetInfo()
            bmpstr = bitmap.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Cleanup
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(window_handle, hwnd_dc)
            
            return img
        except Exception as e:
            raise Exception(f"Failed to capture window: {str(e)}")


if __name__ == "__main__":
    # Test screen capture
    capturer = ScreenCapture()
    img = capturer.capture_screen()
    filename = capturer.save_screenshot(img)
    print(f"Screenshot saved as: {filename}")
