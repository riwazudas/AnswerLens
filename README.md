# Screen Analysis Application with AI Teleprompter

An intelligent application that captures your screen, uses Google Gemini AI to analyze the content, and provides a professional teleprompter for reading AI responses.

## ✨ Features

### Screen Capture
- **Multiple Capture Modes**:
  - Full screen capture
  - Specific window capture (Windows only)
  - Interactive region selection
  - Fixed region for repeated captures
- **Live Preview**: See your captured content instantly
- **Screenshot Export**: Save captures as PNG files

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

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (FREE)

### Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Get a FREE API key:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key

### Running the Application

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
ScreenAnalysis/
├── app.py                 # Main GUI application with teleprompter
├── screen_analyzer.py     # Screen capture functionality
├── llm_analyzer.py        # Google Gemini AI integration
├── region_selector.py     # Interactive region selection tool
├── requirements.txt       # Python dependencies
├── config.json           # Saved configuration (API key)
└── README.md             # This file
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

1. 📝 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 🙏 Acknowledgments

- **Google Gemini**: Powerful free AI vision model
- **Python Community**: Amazing libraries (Pillow, mss, tkinter)
- **Cue Prompter**: Inspiration for teleprompter design

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Google Gemini documentation
3. Open an issue on the repository

## ⭐ Star This Project

If you find this useful, please consider starring the repository!

---

**Built with ❤️ using Python, Google Gemini AI, and Tkinter**d the API key and clicked "Initialize"
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

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to fork, modify, and improve this application!

## Future Enhancements

- Support for region selection with mouse
- History of questions and answers
- Multiple monitor support
- Video/GIF capture and analysis
- OCR integration
- Batch processing of screenshots
- Web interface option
