import tkinter as tk
from app import ScreenAnalysisApp

root = tk.Tk()
app = ScreenAnalysisApp(root)

# Add test text
test_text = "This is test text for scrolling. " * 100
app.answer_text.insert("1.0", test_text)

# Open teleprompter
app.open_teleprompter()

root.mainloop()