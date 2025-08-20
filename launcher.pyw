import tkinter as tk
from tkinter import filedialog
import subprocess
import time
import os
import sys
import webbrowser
try:
    from PIL import ImageGrab
except ModuleNotFoundError: 
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import ImageGrab

def take_screenshot():
    subprocess.run(["powershell", "Start-Process", "ms-screenclip:"])
    wait = 60
    while wait:
        image = ImageGrab.grabclipboard()
        if image is not None:
            break
        time.sleep(1)
        wait -= 1
    print("Ran Take Screenshot")
    read_from_clipboard()

def read_from_clipboard():
    subprocess.Popen("python MGUIDocr.pyw --clipboard".split())
    print("Ran read from clipboard")

def read_from_recent_screenshot():
    subprocess.Popen("python MGUIDocr.pyw --path recent".split())
    print("Ran read from recent")

def open_image():
    screenshots_folder = os.sep.join([os.path.expanduser('~'),r'Pictures\Screenshots'])
    file_path = filedialog.askopenfilename(title="Select a file", initialdir=screenshots_folder)
    subprocess.Popen(['python', 'MGUIDocr.pyw', '--path', file_path])
    print("Ran open image")

def help():
    webbrowser.open("https://github.com/hamsolo474/MGuidOCR/blob/main/README.md")

def close_on_escape(event=None):
    root.destroy()

if __name__ == "__main__":
    print("Starting")
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack(padx=3, pady=3)
    root.bind("<Escape>", close_on_escape)
    title = "MGuidOCR"
    root.title = title
    widgets = []
    widgets.append(tk.Label(frame, text=title, fg="black", font=('Arial', 12), width=0))
    widgets.append(tk.Button(frame, text="Take new screenshot", command=take_screenshot))
    widgets.append(tk.Button(frame, text="Read Image from Clipboard", command=read_from_clipboard))
    widgets.append(tk.Button(frame, text="Read most recent screenshot", command=read_from_recent_screenshot))
    widgets.append(tk.Button(frame, text="Open Image", command=open_image))
    widgets.append(tk.Button(frame, text="Help", command=help))
    for i, widget in enumerate(widgets):
        widget.grid(row=i, column=0, padx=0)
    root.mainloop()
