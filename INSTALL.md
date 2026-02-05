# AnswerLens - Quick Start Guide

## 🚀 Installation (3 Simple Steps)

### Windows Users

1. **Download** this folder to your computer
2. **Double-click** `setup.bat` to install
3. **Double-click** `run.bat` to start AnswerLens

### Linux/Mac Users

1. **Download** this folder to your computer
2. **Open terminal** in this folder and run:
   ```bash
   chmod +x setup.sh run.sh
   ./setup.sh
   ```
3. **Run the app**:
   ```bash
   ./run.sh
   ```

## 📋 Requirements

- **Python 3.8 or higher** - [Download here](https://www.python.org/downloads/)
- **Google Gemini API Key** (FREE) - [Get here](https://aistudio.google.com/apikey)

## 💡 First Time Setup

After installation:

1. Get your FREE API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Open AnswerLens
3. Paste your API key in the "API Key" field
4. Check "Remember" to save it
5. Click "Initialize"
6. Start analyzing screens!

## 📦 What Gets Installed?

- **Virtual Environment** (~50MB) - Isolated Python environment
- **Dependencies** (~30MB) - Required libraries
- **Total Size** - About 80-100MB (much smaller than standalone .exe!)

## ❓ Troubleshooting

**"Python is not installed" error:**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**Setup fails:**
- Make sure you have internet connection
- Try running as administrator (Windows) or with sudo (Linux/Mac)

**Run fails:**
- Make sure you ran setup.bat/setup.sh first
- Check that venv folder exists

## 🔄 Updating

To update to a new version:
1. Download the new version
2. Copy your `config.json` file to the new folder (keeps your API key)
3. Run setup again

## 🗑️ Uninstalling

Simply delete the entire AnswerLens folder. No files are installed elsewhere.

---

For detailed documentation, see [README.md](README.md)
