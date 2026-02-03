"""
Region Selection Tool
Allows user to select a region of the screen with a transparent overlay
"""

import tkinter as tk
from PIL import Image, ImageTk
import mss


class RegionSelector:
    """Tool for selecting a screen region"""
    
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.selected_region = None
        self.root = None
        self.canvas = None
        self.photo = None  # Keep photo reference at class level
    
    def select_region(self):
        """
        Open a transparent overlay to select a region
        
        Returns:
            Tuple of (left, top, width, height) or None if cancelled
        """
        # Take a screenshot of the entire screen using mss
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot_data = sct.grab(monitor)
            screenshot = Image.frombytes('RGB', screenshot_data.size, screenshot_data.rgb)
        
        # Create fullscreen transparent window
        self.root = tk.Toplevel()  # Use Toplevel instead of Tk
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        
        # Create canvas with screenshot
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, 
                                highlightthickness=0, cursor="cross")
        self.canvas.pack()
        
        # Display screenshot - keep reference at class level
        self.photo = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        # Add instructions
        instruction_text = "Click and drag to select region. Press ESC to cancel."
        self.canvas.create_text(screen_width // 2, 30, text=instruction_text, 
                               fill="yellow", font=("Arial", 16, "bold"),
                               tags="instruction")
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", lambda e: self._cancel())
        
        # Wait for window to close
        self.root.wait_window()
        
        # Clean up reference
        self.photo = None
        
        return self.selected_region
    
    def _on_press(self, event):
        """Handle mouse press"""
        self.start_x = event.x
        self.start_y = event.y
        
        # Create rectangle
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="red", width=3, tags="selection"
        )
    
    def _on_drag(self, event):
        """Handle mouse drag"""
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
    
    def _on_release(self, event):
        """Handle mouse release"""
        if self.rect:
            # Get coordinates
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            
            # Ensure x1 < x2 and y1 < y2
            left = int(min(x1, x2))
            top = int(min(y1, y2))
            right = int(max(x1, x2))
            bottom = int(max(y1, y2))
            
            # Calculate width and height
            width = right - left
            height = bottom - top
            
            # Only save if region has size
            if width > 10 and height > 10:
                self.selected_region = (left, top, width, height)
                self.root.destroy()
            else:
                self._cancel()
    
    def _cancel(self):
        """Cancel selection"""
        self.selected_region = None
        self.root.destroy()


if __name__ == "__main__":
    # Test region selector
    selector = RegionSelector()
    region = selector.select_region()
    if region:
        print(f"Selected region: {region}")
    else:
        print("Selection cancelled")
