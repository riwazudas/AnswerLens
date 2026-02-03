"""
GUI Application for Screen Analysis using Google Gemini
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import json
import os
from PIL import Image, ImageTk
from screen_analyzer import ScreenCapture
from llm_analyzer import LLMAnalyzer
from region_selector import RegionSelector


class ScreenAnalysisApp:
    """Main GUI application for screen analysis"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Analysis with Google Gemini")
        self.root.geometry("1200x750")
        
        self.capturer = ScreenCapture()
        self.analyzer = None
        self.selected_window = None
        self.fixed_region = None
        self.current_image = None
        self.current_image_base64 = None
        self.config_file = "config.json"
        self.monitoring = False
        self.monitor_timer = None
        
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """Create the user interface"""
        
        # Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Google Gemini Configuration (FREE)", padding=10)
        config_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # API Key input
        ttk.Label(config_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        api_key_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Remember API Key checkbox
        self.remember_key_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(config_frame, text="Remember", variable=self.remember_key_var).grid(row=0, column=2, padx=5)
        
        # Initialize button
        init_btn = ttk.Button(config_frame, text="Initialize", command=self.initialize_llm)
        init_btn.grid(row=0, column=3, padx=10, pady=5)
        
        self.status_label = ttk.Label(config_frame, text="Status: Not initialized", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # Info label
        info_label = ttk.Label(config_frame, text="💡 Get a FREE API key at: https://aistudio.google.com/apikey", foreground="blue")
        info_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # Screen Capture Frame
        capture_frame = ttk.LabelFrame(self.root, text="Screen Capture Options", padding=10)
        capture_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Capture mode selection
        mode_frame = ttk.Frame(capture_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="Capture Mode:").pack(side=tk.LEFT, padx=5)
        self.capture_mode = tk.StringVar(value="fullscreen")
        ttk.Radiobutton(mode_frame, text="Full Screen", variable=self.capture_mode, 
                       value="fullscreen").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Select Window", variable=self.capture_mode, 
                       value="window").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Select Region", variable=self.capture_mode, 
                       value="region").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Fixed Region", variable=self.capture_mode, 
                       value="fixed").pack(side=tk.LEFT, padx=5)
        
        # Window selection dropdown (for window mode)
        window_frame = ttk.Frame(capture_frame)
        window_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(window_frame, text="Window:").pack(side=tk.LEFT, padx=5)
        self.window_var = tk.StringVar()
        self.window_combo = ttk.Combobox(window_frame, textvariable=self.window_var, 
                                         width=50, state="readonly")
        self.window_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(window_frame, text="Refresh Windows", 
                  command=self.refresh_windows).pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        button_frame = ttk.Frame(capture_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="📷 Capture", 
                  command=self.capture_screen).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🎯 Set Fixed Region", 
                  command=self.set_fixed_region).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save Screenshot", 
                  command=self.save_screenshot).pack(side=tk.LEFT, padx=5)
        
        self.capture_info_label = ttk.Label(capture_frame, text="", foreground="blue")
        self.capture_info_label.pack(fill=tk.X, pady=2)
        
        # Initialize window list if on Windows
        if sys.platform == 'win32':
            self.refresh_windows()
        
        # Create main content frame with two columns
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left column - Question and Answer
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Question Frame
        question_frame = ttk.LabelFrame(left_frame, text="Ask a Question", padding=10)
        question_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(question_frame, text="Question:").pack(anchor=tk.W)
        self.question_text = scrolledtext.ScrolledText(question_frame, height=3, wrap=tk.WORD)
        self.question_text.pack(fill=tk.X, pady=5)
        self.question_text.insert("1.0", "What do you see on this screen?")
        
        # Analysis buttons frame
        analysis_btn_frame = ttk.Frame(question_frame)
        analysis_btn_frame.pack(pady=5)
        
        self.analyze_btn = ttk.Button(analysis_btn_frame, text="Analyze Screen", 
                  command=self.analyze_screen, style="Accent.TButton")
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.monitor_btn = ttk.Button(analysis_btn_frame, text="Start Monitoring (1 min)", 
                  command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=5)
        
        self.monitor_status_label = ttk.Label(question_frame, text="", foreground="green")
        self.monitor_status_label.pack()
        
        ttk.Label(question_frame, text="Answer:").pack(anchor=tk.W)
        self.answer_text = scrolledtext.ScrolledText(question_frame, height=15, wrap=tk.WORD)
        self.answer_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Right column - Preview
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        preview_frame = ttk.LabelFrame(right_frame, text="Screen Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_label = ttk.Label(preview_frame, text="No image captured", 
                                       relief=tk.SUNKEN, anchor=tk.CENTER)
        self.preview_label.pack(fill=tk.BOTH, expand=True)
    
    def load_config(self):
        """Load saved configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key_var.set(config.get('api_key', ''))
                    self.remember_key_var.set(config.get('remember_key', True))
                    
                    # Auto-initialize if API key is saved
                    if config.get('api_key'):
                        self.root.after(100, self.initialize_llm)
        except Exception as e:
            pass  # Ignore config loading errors
    
    def save_config(self):
        """Save configuration"""
        try:
            config = {}
            if self.remember_key_var.get():
                config['api_key'] = self.api_key_var.get()
                config['remember_key'] = True
            else:
                config['api_key'] = ''
                config['remember_key'] = False
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            pass  # Ignore config saving errors
    
    def initialize_llm(self):
        """Initialize the Gemini analyzer"""
        try:
            api_key = self.api_key_var.get() if self.api_key_var.get() else None
            
            self.analyzer = LLMAnalyzer(api_key=api_key)
            
            # Save config if remember is checked
            self.save_config()
            
            self.status_label.config(text="Status: Initialized (Gemini 1.5 Flash)", foreground="green")
            messagebox.showinfo("Success", "Gemini analyzer initialized!\n\nYou can now capture and analyze your screen.")
        except Exception as e:
            self.status_label.config(text="Status: Initialization failed", foreground="red")
            messagebox.showerror("Error", f"Failed to initialize Gemini:\n{str(e)}")
    
    def refresh_windows(self):
        """Refresh the list of available windows"""
        if sys.platform != 'win32':
            messagebox.showwarning("Not Supported", "Window capture is only supported on Windows")
            return
        
        try:
            windows = self.capturer.list_windows()
            # Store window handles and display titles
            self.window_list = windows
            window_titles = [title for _, title in windows]
            self.window_combo['values'] = window_titles
            if window_titles:
                self.window_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list windows:\n{str(e)}")
    
    def set_fixed_region(self):
        """Set a fixed region for capture"""
        try:
            selector = RegionSelector()
            region = selector.select_region()
            if region:
                self.fixed_region = region
                left, top, width, height = region
                self.capture_info_label.config(
                    text=f"✓ Fixed region set: {width}x{height} at ({left}, {top})"
                )
                messagebox.showinfo("Success", f"Fixed region set:\n{width}x{height} pixels at ({left}, {top})")
            else:
                messagebox.showinfo("Cancelled", "Region selection cancelled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to select region:\n{str(e)}")
    
    def capture_screen(self):
        """Capture the screen based on selected mode"""
        try:
            mode = self.capture_mode.get()
            
            if mode == "fullscreen":
                self.current_image = self.capturer.capture_screen()
                self.capture_info_label.config(text="✓ Full screen captured")
            
            elif mode == "window":
                if sys.platform != 'win32':
                    messagebox.showwarning("Not Supported", "Window capture is only supported on Windows")
                    return
                
                # Get selected window
                selected_index = self.window_combo.current()
                if selected_index < 0:
                    messagebox.showwarning("No Window", "Please select a window to capture")
                    return
                
                window_handle, window_title = self.window_list[selected_index]
                self.current_image = self.capturer.capture_window(window_handle)
                self.capture_info_label.config(text=f"✓ Window captured: {window_title}")
            
            elif mode == "region":
                selector = RegionSelector()
                region = selector.select_region()
                if region:
                    left, top, width, height = region
                    self.current_image = self.capturer.capture_region(left, top, width, height)
                    self.capture_info_label.config(text=f"✓ Region captured: {width}x{height}")
                else:
                    messagebox.showinfo("Cancelled", "Region selection cancelled")
                    return
            
            elif mode == "fixed":
                if not self.fixed_region:
                    messagebox.showwarning("No Fixed Region", 
                                         "Please set a fixed region first using 'Set Fixed Region' button")
                    return
                
                left, top, width, height = self.fixed_region
                self.current_image = self.capturer.capture_region(left, top, width, height)
                self.capture_info_label.config(text=f"✓ Fixed region captured: {width}x{height}")
            
            # Convert to base64
            self.current_image_base64 = self.capturer.image_to_base64(self.current_image, max_size=1024)
            
            # Update preview
            self.update_preview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture:\n{str(e)}")
    
    def update_preview(self):
        """Update the preview image"""
        if self.current_image:
            # Resize for preview
            preview_size = (400, 300)
            img_copy = self.current_image.copy()
            img_copy.thumbnail(preview_size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img_copy)
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference
    
    def save_screenshot(self):
        """Save the current screenshot"""
        if self.current_image:
            try:
                filename = self.capturer.save_screenshot(self.current_image)
                messagebox.showinfo("Success", f"Screenshot saved as:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save screenshot:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "No screenshot to save. Capture a screen first.")
    
    def analyze_screen(self):
        """Analyze the captured screen with Gemini"""
        if not self.analyzer:
            messagebox.showwarning("Warning", "Please initialize Gemini first.")
            return
        
        if not self.current_image_base64:
            messagebox.showwarning("Warning", "Please capture a screen first.")
            return
        
        question = self.question_text.get("1.0", tk.END).strip()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question.")
            return
        
        # Show loading message
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", "Analyzing... Please wait...")
        self.root.update()
        
        # Run analysis in a separate thread to avoid freezing UI
        thread = threading.Thread(target=self._analyze_thread, args=(question,))
        thread.daemon = True
        thread.start()
    
    def toggle_monitoring(self):
        """Toggle continuous monitoring on/off"""
        if not self.analyzer:
            messagebox.showwarning("Warning", "Please initialize Gemini first.")
            return
        
        mode = self.capture_mode.get()
        if mode == "region":
            messagebox.showwarning("Warning", "Continuous monitoring not recommended with 'Select Region' mode. Use 'Fixed Region' instead.")
            return
        
        if not self.monitoring:
            # Start monitoring
            self.monitoring = True
            self.monitor_btn.config(text="Stop Monitoring")
            self.monitor_status_label.config(text="🟢 Monitoring active - analyzing every 1 minute")
            self.analyze_btn.config(state="disabled")
            
            # Do first analysis
            self._auto_capture_and_analyze()
        else:
            # Stop monitoring
            self.monitoring = False
            if self.monitor_timer:
                self.root.after_cancel(self.monitor_timer)
                self.monitor_timer = None
            self.monitor_btn.config(text="Start Monitoring (1 min)")
            self.monitor_status_label.config(text="")
            self.analyze_btn.config(state="normal")
    
    def _auto_capture_and_analyze(self):
        """Automatically capture and analyze screen"""
        if not self.monitoring:
            return
        
        try:
            # Auto-capture based on current mode
            mode = self.capture_mode.get()
            
            if mode == "fullscreen":
                self.current_image = self.capturer.capture_screen()
            elif mode == "window":
                if sys.platform == 'win32':
                    selected_index = self.window_combo.current()
                    if selected_index >= 0:
                        window_handle, window_title = self.window_list[selected_index]
                        self.current_image = self.capturer.capture_window(window_handle)
            elif mode == "fixed":
                if self.fixed_region:
                    left, top, width, height = self.fixed_region
                    self.current_image = self.capturer.capture_region(left, top, width, height)
            
            if self.current_image:
                # Convert to base64
                self.current_image_base64 = self.capturer.image_to_base64(self.current_image, max_size=1024)
                
                # Update preview
                self.update_preview()
                
                # Analyze
                question = self.question_text.get("1.0", tk.END).strip()
                if question:
                    # Show analyzing message with timestamp
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.answer_text.delete("1.0", tk.END)
                    self.answer_text.insert("1.0", f"[{timestamp}] Analyzing... Please wait...")
                    self.root.update()
                    
                    # Run analysis
                    thread = threading.Thread(target=self._analyze_thread, args=(question,))
                    thread.daemon = True
                    thread.start()
        
        except Exception as e:
            self.answer_text.delete("1.0", tk.END)
            self.answer_text.insert("1.0", f"Error during auto-capture: {str(e)}")
        
        # Schedule next capture in 60 seconds
        if self.monitoring:
            self.monitor_timer = self.root.after(60000, self._auto_capture_and_analyze)
    
    def _analyze_thread(self, question):
        """Thread function for analysis"""
        try:
            response = self.analyzer.analyze_image(self.current_image_base64, question)
            
            # Add timestamp to response if monitoring
            if self.monitoring:
                from datetime import datetime
                timestamp = datetime.now().strftime("%H:%M:%S")
                response = f"[{timestamp}] {response}"
            
            self.root.after(0, self._update_answer, response)
        except Exception as e:
            self.root.after(0, self._show_error, str(e))
    
    def _update_answer(self, response):
        """Update the answer text box"""
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", response)
    
    def _show_error(self, error_msg):
        """Show error message"""
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", f"Error: {error_msg}")
        messagebox.showerror("Analysis Error", f"Failed to analyze screen:\n{error_msg}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ScreenAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
