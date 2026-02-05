"""
AnswerLens - AI Screen Analysis Application
GUI Application using Google Gemini
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
    """AnswerLens - Main GUI application for AI screen analysis"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AnswerLens - AI Screen Analysis")
        self.root.geometry("1200x750")
        
        # Set window icon (logo) - store as instance variable to prevent garbage collection
        self.icon_image = None
        try:
            # Try PNG format (cross-platform)
            if os.path.exists("logo.png"):
                self.icon_image = tk.PhotoImage(file="logo.png")
                self.root.iconphoto(True, self.icon_image)
            elif os.path.exists("logo.ico"):
                # For Windows: use .ico file
                self.root.iconbitmap("logo.ico")
        except Exception as e:
            print(f"Could not load logo: {e}")
            pass  # No icon file found, use default
        
        self.capturer = ScreenCapture()
        self.analyzer = None
        self.selected_window = None
        self.fixed_region = None
        self.current_image = None
        self.current_image_base64 = None
        self.config_file = "config.json"
        self.monitoring = False
        self.monitor_timer = None
        self.teleprompter_window = None
        self.teleprompter_scroll_active = False
        self.teleprompter_scroll_timer = None
        self.teleprompter_word_timer = None
        self.teleprompter_controls_visible = True
        self.current_word_index = 0
        self.word_positions = []
        self.scroll_delay_counter = 0
        
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
        self.question_text.insert("1.0", "What do you see on this screen? Give answer in around 100 words and make it into a single paragraph")
        
        # Analysis buttons frame
        analysis_btn_frame = ttk.Frame(question_frame)
        analysis_btn_frame.pack(pady=5)
        
        self.analyze_btn = ttk.Button(analysis_btn_frame, text="Analyze Screen", 
                  command=self.analyze_screen, style="Accent.TButton")
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.monitor_btn = ttk.Button(analysis_btn_frame, text="Start Monitoring (1 min)", 
                  command=self.toggle_monitoring)
        self.monitor_btn.pack(side=tk.LEFT, padx=5)
        
        self.teleprompter_btn = ttk.Button(analysis_btn_frame, text="📖 Teleprompter", 
                  command=self.open_teleprompter)
        self.teleprompter_btn.pack(side=tk.LEFT, padx=5)
        
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
    
    def open_teleprompter(self):
        """Open or focus the teleprompter window"""
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            # If window exists, just focus it
            self.teleprompter_window.lift()
            self.teleprompter_window.focus_force()
        else:
            # Create new teleprompter window
            self.create_teleprompter_window()
    
    def create_teleprompter_window(self):
        """Create the teleprompter-style floating window"""
        self.teleprompter_window = tk.Toplevel(self.root)
        self.teleprompter_window.title("Teleprompter")
        
        # Window dimensions - fixed size for consistent viewing
        window_width = 600
        window_height = 400
        
        # Center the window on screen
        screen_width = self.teleprompter_window.winfo_screenwidth()
        screen_height = self.teleprompter_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3  # Positioned upper-center like Spotlight
        
        self.teleprompter_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Window styling - clean and minimal with transparency
        self.teleprompter_window.configure(bg='#2b2b2b')
        self.teleprompter_window.attributes('-alpha', 0.92)  # 92% opacity (slightly see-through)
        
        # Make window fixed size (not resizable)
        self.teleprompter_window.resizable(False, False)
        
        # Add rounded corner effect with shadow (visual only)
        main_frame = tk.Frame(self.teleprompter_window, bg='#2b2b2b', highlightthickness=2, 
                             highlightbackground='#404040')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header with close button
        header_frame = tk.Frame(main_frame, bg='#2b2b2b', height=40)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📖 Teleprompter View", 
                              bg='#2b2b2b', fg='#ffffff', font=('Segoe UI', 12, 'bold'))
        title_label.pack(side=tk.LEFT, pady=5)
        
        close_btn = tk.Button(header_frame, text="✕", command=self.teleprompter_window.destroy,
                             bg='#2b2b2b', fg='#888888', font=('Segoe UI', 14), 
                             bd=0, cursor='hand2', padx=10, pady=0)
        close_btn.pack(side=tk.RIGHT)
        
        # Hide controls button
        hide_btn = tk.Button(header_frame, text="⚙", command=self.toggle_teleprompter_controls,
                             bg='#2b2b2b', fg='#888888', font=('Segoe UI', 14), 
                             bd=0, cursor='hand2', padx=10, pady=0)
        hide_btn.pack(side=tk.RIGHT, padx=5)
        
        # Hover effects for buttons
        def on_enter_close(e):
            close_btn.config(fg='#ff5555')
        def on_leave_close(e):
            close_btn.config(fg='#888888')
        def on_enter_hide(e):
            hide_btn.config(fg='#ffffff')
        def on_leave_hide(e):
            hide_btn.config(fg='#888888')
        close_btn.bind('<Enter>', on_enter_close)
        close_btn.bind('<Leave>', on_leave_close)
        hide_btn.bind('<Enter>', on_enter_hide)
        hide_btn.bind('<Leave>', on_leave_hide)
        
        # Separator line
        separator = tk.Frame(main_frame, bg='#404040', height=1)
        separator.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Text display area with scrollbar
        text_container = tk.Frame(main_frame, bg='#2b2b2b')
        text_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Create scrollbar (hidden but functional)
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for content
        self.teleprompter_text = tk.Text(text_container, wrap=tk.WORD, 
                                         bg='#1a1a1a', fg='#e0e0e0',
                                         font=('Arial', 24, 'normal'), bd=0,
                                         padx=30, pady=60, spacing3=10,
                                         insertbackground='#e0e0e0',
                                         relief=tk.FLAT,
                                         yscrollcommand=scrollbar.set)
        self.teleprompter_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.teleprompter_text.yview)
        
        # Hide the scrollbar visually but keep it functional
        scrollbar.pack_forget()
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(width=0)  # Make scrollbar invisible
        
        # Control buttons frame
        self.teleprompter_control_frame = tk.Frame(main_frame, bg='#2b2b2b')
        self.teleprompter_control_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        control_frame = self.teleprompter_control_frame
        
        # Play/Pause button
        self.scroll_toggle_btn = tk.Button(control_frame, text="▶ Play",
                                           command=self.toggle_teleprompter_scroll,
                                           bg='#00aa00', fg='#ffffff',
                                           font=('Segoe UI', 10, 'bold'), bd=0,
                                           cursor='hand2', padx=20, pady=8)
        self.scroll_toggle_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        reset_btn = tk.Button(control_frame, text="⟲ Reset",
                             command=self.reset_teleprompter,
                             bg='#404040', fg='#ffffff',
                             font=('Segoe UI', 10), bd=0,
                             cursor='hand2', padx=15, pady=8)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Speed controls
        speed_label = tk.Label(control_frame, text="Speed:", bg='#2b2b2b', 
                              fg='#cccccc', font=('Segoe UI', 10, 'bold'))
        speed_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.scroll_speed_var = tk.IntVar(value=3)
        speed_slider = tk.Scale(control_frame, from_=0, to=10,
                               orient=tk.HORIZONTAL, variable=self.scroll_speed_var,
                               bg='#2b2b2b', fg='#cccccc', troughcolor='#404040',
                               highlightthickness=0, showvalue=True, length=120,
                               width=15, resolution=0.5)
        speed_slider.pack(side=tk.LEFT, padx=5)
        
        # Font size controls
        font_label = tk.Label(control_frame, text="Size:", bg='#2b2b2b', 
                             fg='#cccccc', font=('Segoe UI', 10, 'bold'))
        font_label.pack(side=tk.LEFT, padx=(20, 5))
        
        font_minus_btn = tk.Button(control_frame, text="−",
                                   command=lambda: self.adjust_font_size(-2),
                                   bg='#404040', fg='#ffffff',
                                   font=('Segoe UI', 12, 'bold'), bd=0,
                                   cursor='hand2', padx=10, pady=5)
        font_minus_btn.pack(side=tk.LEFT, padx=2)
        
        font_plus_btn = tk.Button(control_frame, text="+",
                                  command=lambda: self.adjust_font_size(2),
                                  bg='#404040', fg='#ffffff',
                                  font=('Segoe UI', 12, 'bold'), bd=0,
                                  cursor='hand2', padx=10, pady=5)
        font_plus_btn.pack(side=tk.LEFT, padx=2)
        
        # Insert current answer if available
        current_answer = self.answer_text.get("1.0", tk.END).strip()
        if current_answer:
            self.teleprompter_text.insert("1.0", current_answer)
            # Configure tag for highlighted word
            self.teleprompter_text.tag_config("highlight", background="#ffff00", foreground="#000000", font=('Arial', 24, 'normal'))
            self._parse_words()
        else:
            self.teleprompter_text.insert("1.0", "No response available yet.\n\nAnalyze a screen to see the results here.")
            self.teleprompter_text.tag_add("center", "1.0", "end")
            self.teleprompter_text.tag_config("center", justify='center', foreground='#888888')
        
        # Make text read-only but allow selection
        self.teleprompter_text.config(state=tk.NORMAL)
        
        # Enable dragging the window
        def start_move(event):
            self.teleprompter_window.x = event.x
            self.teleprompter_window.y = event.y
        
        def do_move(event):
            deltax = event.x - self.teleprompter_window.x
            deltay = event.y - self.teleprompter_window.y
            x = self.teleprompter_window.winfo_x() + deltax
            y = self.teleprompter_window.winfo_y() + deltay
            self.teleprompter_window.geometry(f"+{x}+{y}")
        
        header_frame.bind('<Button-1>', start_move)
        header_frame.bind('<B1-Motion>', do_move)
        title_label.bind('<Button-1>', start_move)
        title_label.bind('<B1-Motion>', do_move)
        
        # Keep window on top
        self.teleprompter_window.attributes('-topmost', True)
        
        # Keyboard shortcuts
        self.teleprompter_window.bind('<Escape>', lambda e: self.teleprompter_window.destroy())
        self.teleprompter_window.bind('<space>', lambda e: self.toggle_teleprompter_scroll())
        
        # Cleanup when window closes
        self.teleprompter_window.protocol("WM_DELETE_WINDOW", self.close_teleprompter)
        
        # Auto-start scrolling after 5 seconds
        self.root.after(5000, self._auto_start_teleprompter)
    
    # Sync feature removed - teleprompter content is set once when window opens
    # def _sync_teleprompter(self):
    #     """Continuously sync the teleprompter with the main answer text"""
    #     pass
    
    def _auto_start_teleprompter(self):
        """Auto-start scrolling after delay"""
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            # Only start if not already scrolling and we have words to highlight
            if not self.teleprompter_scroll_active and len(self.word_positions) > 0:
                self.toggle_teleprompter_scroll()
    
    def toggle_teleprompter_scroll(self):
        """Toggle automatic scrolling in teleprompter"""
        if not hasattr(self, 'teleprompter_scroll_active'):
            return
            
        self.teleprompter_scroll_active = not self.teleprompter_scroll_active
        
        if self.teleprompter_scroll_active:
            self.scroll_toggle_btn.config(text="⏸ Pause", bg='#cc0000')
            # Reset delay counter when starting
            self.scroll_delay_counter = 0
            # Start both continuous scrolling and word highlighting
            self._continuous_scroll()
            self._highlight_next_word()
        else:
            self.scroll_toggle_btn.config(text="▶ Play", bg='#00aa00')
            # Cancel both timers
            if self.teleprompter_scroll_timer:
                self.root.after_cancel(self.teleprompter_scroll_timer)
                self.teleprompter_scroll_timer = None
            if self.teleprompter_word_timer:
                self.root.after_cancel(self.teleprompter_word_timer)
                self.teleprompter_word_timer = None
    
    def _continuous_scroll(self):
        """Continuously scroll the text at a fixed smooth speed"""
        if not self.teleprompter_scroll_active:
            return
        
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            try:
                # Get current scroll position
                yview_result = self.teleprompter_text.yview()
                if not yview_result or len(yview_result) < 2:
                    # Invalid yview result, skip this frame
                    self.teleprompter_scroll_timer = self.root.after(50, self._continuous_scroll)
                    return
                    
                current_pos = yview_result[0]
                
                # Sanity check: ensure position is valid
                if current_pos < 0 or current_pos > 1:
                    # Invalid position, don't scroll this frame
                    self.teleprompter_scroll_timer = self.root.after(50, self._continuous_scroll)
                    return
                
                # Check if we've reached the end - just stop, don't reset
                if current_pos >= 0.95:
                    # Stop scrolling without resetting position
                    self.teleprompter_scroll_active = False
                    self.scroll_toggle_btn.config(text="▶ Play", bg='#00aa00')
                    if self.teleprompter_scroll_timer:
                        self.root.after_cancel(self.teleprompter_scroll_timer)
                        self.teleprompter_scroll_timer = None
                    if self.teleprompter_word_timer:
                        self.root.after_cancel(self.teleprompter_word_timer)
                        self.teleprompter_word_timer = None
                    return
                
                # Delay scrolling for first 3 seconds (60 frames at 50ms) so first line completes
                if self.scroll_delay_counter < 60:
                    self.scroll_delay_counter += 1
                    self.teleprompter_scroll_timer = self.root.after(50, self._continuous_scroll)
                    return
                
                # Calculate scroll speed based on slider (0-10)
                speed_value = self.scroll_speed_var.get()
                # Slightly increased scroll speed
                scroll_increment = 0.00009 + (speed_value * 0.0001)  # Range: 0.00009 to 0.00109
                
                # Scroll smoothly
                self.teleprompter_text.yview_moveto(current_pos + scroll_increment)
                
                # Schedule next scroll (fixed 50ms for smooth animation)
                self.teleprompter_scroll_timer = self.root.after(100, self._continuous_scroll)
            except:
                self.teleprompter_scroll_active = False
    
    def _highlight_next_word(self):
        """Highlight the next word based on speed"""
        if not self.teleprompter_scroll_active:
            return
        
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            try:
                # Check if we have words to highlight
                if not self.word_positions or self.current_word_index >= len(self.word_positions):
                    return
                
                # Remove previous highlight
                self.teleprompter_text.tag_remove("highlight", "1.0", tk.END)
                
                # Highlight current word
                start_pos, end_pos = self.word_positions[self.current_word_index]
                self.teleprompter_text.tag_add("highlight", start_pos, end_pos)
                
                # Calculate delay based on speed slider (0-10 range)
                speed_value = self.scroll_speed_var.get()
                # Convert speed: higher value = faster (shorter delay)
                # Reduced delay for faster word highlighting
                delay = max(80, int(600 - (speed_value * 50)))
                
                # Move to next word
                self.current_word_index += 1
                
                # Schedule next word highlight
                self.teleprompter_word_timer = self.root.after(delay, self._highlight_next_word)
            except Exception as e:
                print(f"Word highlight error: {e}")
    
    def reset_teleprompter(self):
        """Reset teleprompter to beginning"""
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            # Stop scrolling if active
            if self.teleprompter_scroll_active:
                self.toggle_teleprompter_scroll()
            
            # Remove all highlights
            self.teleprompter_text.tag_remove("highlight", "1.0", tk.END)
            
            # Reset word index, scroll counter, and scroll to top
            self.current_word_index = 0
            self.scroll_delay_counter = 0
            self.teleprompter_text.yview_moveto(0)
    
    def _parse_words(self):
        """Parse text content and store word positions for highlighting"""
        import re
        self.word_positions = []
        
        # Get all text content
        text = self.teleprompter_text.get("1.0", tk.END)
        
        # Find all words with their positions
        for match in re.finditer(r'\S+', text):
            start_idx = match.start()
            end_idx = match.end()
            
            # Convert character positions to Tkinter text indices
            start_pos = f"1.0 + {start_idx} chars"
            end_pos = f"1.0 + {end_idx} chars"
            
            self.word_positions.append((start_pos, end_pos))
        
        self.current_word_index = 0
    
    def toggle_teleprompter_controls(self):
        """Toggle visibility of teleprompter control panel"""
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            self.teleprompter_controls_visible = not self.teleprompter_controls_visible
            
            if self.teleprompter_controls_visible:
                self.teleprompter_control_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
            else:
                self.teleprompter_control_frame.pack_forget()
    
    def adjust_font_size(self, delta):
        """Adjust the teleprompter font size"""
        if self.teleprompter_window and self.teleprompter_window.winfo_exists():
            current_font = self.teleprompter_text['font']
            # Parse font tuple
            font_parts = current_font.split()
            if len(font_parts) >= 2:
                font_family = font_parts[0]
                try:
                    font_size = int(font_parts[1])
                    new_size = max(12, min(48, font_size + delta))  # Limit between 12 and 48
                    self.teleprompter_text.config(font=(font_family, new_size, 'normal'))
                except:
                    pass
    
    def close_teleprompter(self):
        """Clean up and close teleprompter window"""
        self.teleprompter_scroll_active = False
        if self.teleprompter_scroll_timer:
            self.root.after_cancel(self.teleprompter_scroll_timer)
            self.teleprompter_scroll_timer = None
        if self.teleprompter_word_timer:
            self.root.after_cancel(self.teleprompter_word_timer)
            self.teleprompter_word_timer = None
        if self.teleprompter_window:
            self.teleprompter_window.destroy()
            self.teleprompter_window = None


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ScreenAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
