# AnswerLens - AI Screen Analysis with Teleprompter

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/riwazudas/AnswerLens/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

An intelligent application that captures your screen, uses Google Gemini AI to analyze the content, and provides a professional teleprompter for reading AI responses.

## 📑 Table of Contents

- [System Requirements](#-system-requirements)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Use Cases](#-use-cases)
- [Teleprompter Tips](#-teleprompter-tips)
- [Project Structure](#-project-structure)
- [Advanced Usage](#-advanced-usage)
- [Distribution & Deployment](#-distribution--deployment)
- [Documentation](#-documentation)
- [Troubleshooting](#️-troubleshooting)
- [Security & Privacy](#-security--privacy)
- [Customization](#-customization)
- [Version History](#-version-history)
- [Contributing](#-contributing)
- [Future Enhancements](#-future-enhancements)
- [Acknowledgments](#-acknowledgments)
- [Support](#-support)

## 💻 System Requirements

- **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.14+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100-200MB for application and dependencies
- **Internet**: Required for Google Gemini API access
- **Display**: Any resolution (1920x1080+ recommended for best experience)

### Dependencies

All dependencies are automatically installed via `requirements.txt`:
- `tkinter` - GUI framework (usually included with Python)
- `Pillow` - Image processing
- `mss` - Fast screen capture
- `google-generativeai` - Google Gemini AI SDK
- `pywin32` - Windows-specific features (Windows only)

## ✨ Features

### Screen Capture
- **Multiple Capture Modes**:
  - Full screen capture
  - Specific window capture (Windows only)
  - Interactive region selection
  - Fixed region for repeated captures
- **Live Preview**: See your captured content instantly
- **Screenshot Export**: Save captures as PNG files
- **Custom Logo**: Branded application icon for professional appearance

### AI Analysis with Google Gemini
- **FREE API**: Uses Google Gemini 1.5 Flash (completely free)
- **Vision AI**: Analyzes screenshots and answers questions about content
- **Continuous Monitoring**: Auto-capture and analyze every minute
- **Context-Aware**: Provides detailed, intelligent responses about screen content

### 📖 Professional Teleprompter
- **Cue Prompter Style**: Reading line marker for focused reading
- **Auto-Scroll**: Smooth automatic scrolling with adjustable speed (0-10)
- **Auto-Start**: Begins scrolling automatically after 5 seconds
- **Customizable Display**:
  - Adjustable font size (12-48pt)
  - Resizable window
  - Semi-transparent overlay (92% opacity)
  - Always-on-top mode
- **Reading Line**: Red horizontal marker shows current reading position
- **Control Panel**: Show/hide settings for distraction-free reading
- **Keyboard Shortcuts**:
  - `Space` - Play/Pause scrolling
  - `Escape` - Close teleprompter

## 🚀 Quick Start

### Method 1: Easy Installation (Recommended)

**Windows Users:**
1. Download or clone this repository
2. Double-click `setup.bat` to install
3. Double-click `run.bat` to start AnswerLens

**Linux/Mac Users:**
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

📖 **See [INSTALL.md](INSTALL.md) for detailed instructions**

### Method 2: Manual Installation

#### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (FREE)

#### Steps

1. Clone or download this repository

2. Create virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Get a FREE API key:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key

5. Run the application:
```bash
python app.py
```

## 📖 Usage Guide

### Initial Setup

1. **Initialize Gemini AI**:
   - Paste your API key in the "API Key" field
   - Check "Remember" to save it for future sessions
   - Click "Initialize"
   - Status will show green when ready

### Capturing Screens

2. **Choose Capture Mode**:
   - **Full Screen**: Capture entire display
   - **Select Window**: Choose a specific application window (Windows)
   - **Select Region**: Draw a rectangle to select area
   - **Fixed Region**: Set a region once, capture repeatedly

3. **Take Screenshot**:
   - Click "📷 Capture" button
   - View preview in the right panel

### Analyzing Content

4. **Ask Questions**:
   - Type your question (default: "What do you see on this screen?")
   - Click "Analyze Screen"
   - Read the AI response

### Using the Teleprompter

5. **Open Teleprompter**:
   - Click "📖 Teleprompter" button
   - Window opens with current AI response
   - Automatically starts scrolling after 5 seconds

6. **Teleprompter Controls**:
   - **▶ Play / ⏸ Pause**: Start/stop auto-scrolling
   - **⟲ Reset**: Jump back to beginning
   - **Speed Slider**: Adjust scroll speed (0=slowest, 10=fastest)
   - **− / +**: Decrease/increase font size
   - **⚙ Gear Icon**: Hide/show control panel
   - **Resize Window**: Drag corners to resize

### Continuous Monitoring

7. **Auto-Monitor Mode**:
   - Click "Start Monitoring (1 min)"
   - Application captures and analyzes every 60 seconds
   - Perfect for monitoring changing content
   - Click "Stop Monitoring" to end

## 💡 Use Cases

- **Accessibility**: Screen reader enhancement with AI descriptions
- **Presentations**: Read AI-generated notes via teleprompter
- **Learning**: Get explanations about code, diagrams, or tutorials
- **Documentation**: Generate descriptions of UI elements and workflows
- **Troubleshooting**: Analyze error messages and system dialogs
- **Content Creation**: Review and read AI-generated content smoothly
- **Data Extraction**: Extract and analyze information from screenshots
- **Monitoring**: Continuous analysis of changing screen content

## 🎯 Teleprompter Tips

- **Optimal Speed**: Start with speed 3, adjust to your reading pace
- **Font Size**: Use + / − buttons to find comfortable size
- **Hide Controls**: Click ⚙ for distraction-free reading
- **Window Size**: Resize to fit your screen layout
- **Transparency**: See through window to view background content
- **Reading Line**: Focus on the red line marker while reading

## 📁 Project Structure

```
AnswerLens/
├── app.py                 # Main GUI application with teleprompter
├── screen_analyzer.py     # Screen capture functionality
├── llm_analyzer.py        # Google Gemini AI integration
├── region_selector.py     # Interactive region selection tool
├── build_exe.py          # PyInstaller build script
├── AnswerLens.spec       # PyInstaller specification
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup configuration
├── config.json           # Saved configuration (API key)
├── logo.png              # Application icon
├── setup.bat             # Windows setup script
├── run.bat               # Windows run script
├── setup.sh              # Linux/Mac setup script
├── run.sh                # Linux/Mac run script
├── README.md             # This file
├── INSTALL.md            # Quick start guide for end users
├── DEPLOYMENT.md         # Comprehensive deployment guide
├── CHANGELOG.md          # Version history and changes
└── LICENSE               # License information
```

## 🔧 Advanced Usage

### Use as Python Library

```python
from screen_analyzer import ScreenCapture
from llm_analyzer import LLMAnalyzer

# Capture screen
capturer = ScreenCapture()
img = capturer.capture_screen()
img_base64 = capturer.image_to_base64(img)

# Analyze with Gemini
analyzer = LLMAnalyzer(api_key='your-api-key')
response = analyzer.analyze_image(img_base64, "What do you see?")
print(response)
```

### Environment Variable (Optional)

Set API key as environment variable:

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key"

# Windows Command Prompt
set GEMINI_API_KEY=your-api-key

# Linux/Mac
export GEMINI_API_KEY="your-api-key"
```

### Fixed Region for Monitoring

1. Click "🔧 Set Fixed Region"
2. Draw a rectangle on your screen
3. Use "📷 Capture" repeatedly without re-selecting
4. Perfect for monitoring specific screen areas

## 📦 Distribution & Deployment

### For End Users

Want to share AnswerLens with others? We offer multiple distribution methods:

#### Option 1: Virtual Environment Distribution (Recommended)
- ✅ **Smallest size**: ~5MB source + ~80MB dependencies
- ✅ **Easy updates**: Just replace Python files
- ✅ **No antivirus issues**: No false positives
- ✅ **Cross-platform**: Works on Windows, Linux, macOS

Package includes: Python files + simple scripts (`setup.bat`, `run.bat`)

#### Option 2: Standalone Executable
- ⚠️ **Large size**: ~100-150MB per platform
- ⚠️ **May trigger antivirus**: False positives common
- Build using: `python build_exe.py`

#### Option 3: Python Package
- Install via pip after packaging
- Suitable for Python developers
- Build using: `python setup.py sdist bdist_wheel`

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide**

### Build Executable (Optional)

To create a standalone executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Output in dist/AnswerLens.exe (Windows) or dist/AnswerLens (Linux/Mac)
```

## 📄 Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[INSTALL.md](INSTALL.md)** - Quick start guide for end users
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment and distribution guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

## 📝 License

This project is provided as-is for educational and personal use. See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## �️ Troubleshooting

**"API key is invalid" error**:
- Ensure you pasted the API key and clicked "Initialize"
- Check that you copied the complete key from Google AI Studio

**"Failed to capture screen" error**:
- Run as administrator (Windows)
- Check screen recording permissions (macOS)
- Close conflicting screen capture applications

**Teleprompter not starting**:
- Ensure you've analyzed a screen first
- Check if window is hidden behind other windows
- Try closing and reopening the teleprompter

**Window capture not available**:
- Window capture is Windows-only
- Use "Select Region" or "Fixed Region" on other platforms

**Import errors**:
- Run: `pip install -r requirements.txt`
- Ensure all files are in the same directory
- Check Python version (3.8+ required)

## 🔒 Security & Privacy

- **API Key Storage**: Keys saved locally in `config.json` (optional)
- **Data Privacy**: Screenshots sent to Google Gemini API
- **No Tracking**: No telemetry or usage tracking
- **Local Processing**: All capture processing done locally
- **Best Practice**: Use environment variables for API keys in production

## 🎨 Customization

### Teleprompter Appearance

Edit `app.py` to customize:
- Background color: `bg='#1a1a1a'`
- Text color: `fg='#e0e0e0'`  
- Reading line color: `fill='#ff5252'`
- Font family: `font=('Arial', 24)`
- Transparency: `attributes('-alpha', 0.92)`

### Scroll Speed

Default speed (0-10 scale):
```python
self.scroll_speed_var = tk.IntVar(value=3)
```

### Auto-start Delay

Change 5-second delay:
```python
self.root.after(5000, self._auto_start_teleprompter)  # 5000ms = 5 seconds
```

## 📊 Version History

### Current Version: 1.0.0 (Released: February 4, 2026)

**Major Features:**
- ✅ Screen capture (fullscreen, window, region, fixed region)
- ✅ Google Gemini AI integration
- ✅ Professional teleprompter with auto-scroll
- ✅ Live preview and screenshot export
- ✅ Continuous monitoring mode
- ✅ Logo/icon support
- ✅ Cross-platform compatibility
- ✅ Simple setup scripts for easy installation
- ✅ Multiple deployment options

📖 **See [CHANGELOG.md](CHANGELOG.md) for complete version history**

## 🤝 Contributing

Contributions welcome! Feel free to:
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features and enhancements
- 🔧 Submit pull requests
- 📖 Improve documentation
- ⭐ Star the repository if you find it useful

### Development Setup

```bash
# Clone repository
git clone https://github.com/riwazudas/AnswerLens.git
cd AnswerLens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🔮 Future Enhancements

Planned features for future releases:
- Multiple monitor support
- History of questions and answers
- Video/GIF capture and analysis
- OCR integration
- Batch processing of screenshots
- Web interface option
- Custom keyboard shortcuts
- Dark/light theme toggle
- Export responses to various formats

## 🙏 Acknowledgments

- **Google Gemini**: Powerful free AI vision model
- **Python Community**: Amazing libraries (Pillow, mss, tkinter)
- **Cue Prompter**: Inspiration for teleprompter design

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#🛠️-troubleshooting) section
2. Review [Google Gemini documentation](https://ai.google.dev/docs)
3. Open an issue on the [GitHub repository](https://github.com/riwazudas/AnswerLens/issues)

## ⭐ Star This Project

If you find AnswerLens useful, please consider starring the repository!

---

**Built with ❤️ using Python, Google Gemini AI, and Tkinter**

