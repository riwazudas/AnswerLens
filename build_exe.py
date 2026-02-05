"""
Build standalone executable for AnswerLens
Requires: pip install pyinstaller
Usage: python build_exe.py
"""

import PyInstaller.__main__
import os
import sys

def build():
    """Build standalone executable"""
    
    # Base arguments for PyInstaller
    args = [
        'app.py',                          # Main script
        '--name=AnswerLens',               # Name of the executable
        '--windowed',                      # Hide console window (GUI app)
        '--onefile',                       # Single executable file
        '--icon=logo.png',                 # Application icon
        '--add-data=logo.png;.',          # Include logo (Windows)
        '--add-data=README.md;.',         # Include README
        '--hidden-import=PIL._tkinter_finder',  # Ensure PIL/Tkinter compatibility
        '--hidden-import=google.genai',   # Include Gemini AI
        '--hidden-import=mss',            # Screen capture
        '--clean',                         # Clean PyInstaller cache
        '--noconfirm',                     # Overwrite without asking
    ]
    
    # Platform-specific adjustments
    if sys.platform == 'win32':
        # Windows-specific
        args.append('--hidden-import=win32gui')
        args.append('--hidden-import=win32con')
    elif sys.platform == 'darwin':
        # macOS - use colon separator
        args[6] = '--add-data=logo.png:.'
        args[7] = '--add-data=README.md:.'
    else:
        # Linux - use colon separator
        args[6] = '--add-data=logo.png:.'
        args[7] = '--add-data=README.md:.'
    
    print("Building AnswerLens executable...")
    print("This may take a few minutes...")
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("\n✅ Build complete!")
    print("Executable location: dist/AnswerLens.exe (Windows) or dist/AnswerLens (Linux/Mac)")
    print("\nTo distribute:")
    print("1. Copy the entire 'dist' folder")
    print("2. Include logo.png in the same directory as the executable")
    print("3. Users will need a Google Gemini API key to use the app")

if __name__ == "__main__":
    build()
