# Screen Analysis Application

An intelligent application that captures your screen and uses Large Language Models (LLMs) to analyze the content and answer questions about what's displayed.

## Features

- **Screen Capture**: Capture full screen or specific regions
- **LLM Integration**: Supports OpenAI GPT-4 Vision and Anthropic Claude
- **Interactive GUI**: User-friendly interface built with Tkinter
- **Question & Answer**: Ask questions about your screen content and get intelligent responses
- **Screenshot Management**: Save captured screenshots for later reference

## Prerequisites

- Python 3.8 or higher
- API key from OpenAI or Anthropic

## Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Get an API key:
   - **OpenAI**: Sign up at [platform.openai.com](https://platform.openai.com/) and generate an API key
   - **Anthropic**: Sign up at [console.anthropic.com](https://console.anthropic.com/) and generate an API key

## Usage

### Running the Application

```bash
python app.py
```

### Using the GUI

1. **Configure LLM**:
   - Select your preferred provider (OpenAI or Anthropic)
   - Enter your API key
   - Click "Initialize LLM"

2. **Capture Screen**:
   - Click "Capture Full Screen" to take a screenshot
   - The preview will appear in the preview panel

3. **Ask Questions**:
   - Type your question in the question box
   - Click "Analyze Screen" to get an AI-powered answer
   - The response will appear in the answer box

4. **Save Screenshots** (optional):
   - Click "Save Screenshot" to save the current capture

### Alternative: Use as Library

You can also use the components programmatically:

```python
from screen_analyzer import ScreenCapture
from llm_analyzer import LLMAnalyzer

# Capture screen
capturer = ScreenCapture()
img = capturer.capture_screen()
img_base64 = capturer.image_to_base64(img)

# Analyze with LLM
analyzer = LLMAnalyzer(provider='anthropic', api_key='your-api-key')
response = analyzer.analyze_image(img_base64, "What do you see on this screen?")
print(response)
```

## Environment Variables

You can set API keys as environment variables instead of entering them in the GUI:

**Windows (PowerShell)**:
```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:ANTHROPIC_API_KEY="your-anthropic-key"
```

**Windows (Command Prompt)**:
```cmd
set OPENAI_API_KEY=your-openai-key
set ANTHROPIC_API_KEY=your-anthropic-key
```

**Linux/Mac**:
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## Project Structure

```
ScreenAnalysis/
├── app.py                 # Main GUI application
├── screen_analyzer.py     # Screen capture functionality
├── llm_analyzer.py        # LLM integration (OpenAI, Anthropic)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Example Use Cases

- **Accessibility**: Describe screen content for visually impaired users
- **Documentation**: Generate descriptions of UI elements
- **Troubleshooting**: Ask questions about error messages or dialogs
- **Learning**: Get explanations about code, diagrams, or content on screen
- **Data Extraction**: Extract text or information from screenshots
- **Design Review**: Get feedback on UI designs and layouts

## API Costs

Both OpenAI and Anthropic charge for API usage:
- **OpenAI GPT-4 Vision**: Check current pricing at [openai.com/pricing](https://openai.com/pricing)
- **Anthropic Claude**: Check current pricing at [anthropic.com/pricing](https://www.anthropic.com/pricing)

Images are automatically resized to reduce costs while maintaining quality.

## Troubleshooting

**"API key not found" error**:
- Make sure you've entered the API key in the GUI or set it as an environment variable

**"Failed to capture screen" error**:
- Ensure you have proper screen capture permissions on your system
- On macOS, you may need to grant Screen Recording permissions in System Preferences

**Import errors**:
- Run `pip install -r requirements.txt` to install all dependencies

**"Module not found" errors**:
- Make sure all files (app.py, screen_analyzer.py, llm_analyzer.py) are in the same directory

## Security Note

- Never share your API keys publicly
- API keys in the GUI are displayed as asterisks but stored in memory
- Consider using environment variables for better security

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
