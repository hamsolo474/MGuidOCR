import os
import tkinter as tk
import argparse
import subprocess
import sys
try:
    import PIL
    from PIL import ImageGrab
    import pytesseract
    import pyperclip
except ModuleNotFoundError: 
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "pytesseract", "pillow"])
    import PIL
    from PIL import ImageGrab
    import pytesseract
    import pyperclip
#import win10toast
#import clipboard_monitor

def fix(s):
    s = s.replace('s','5')
    s = s.replace('S','5')
    s = s.replace('$','5')
    s = s.replace('l','1') # this is lowercase L
    s = s.replace('I','1')
    s = s.replace('i','1')
    s = s.replace('A','4')
    s = s.replace('O','0')
    s = s.replace('o','0')
    s = s.replace('B','3')
    s = s.replace(' ','')
    s = s.replace('"','')
    s = s.replace("'",'')
    s = s.replace('¢','c')
    s = s.replace('.','')
    s = s.replace(':','')
    s = s.replace('/','')
    s = s.replace('*','')
    s = s.lower()
    return s

def validate_text(text, func, row=0):
    for i, char in enumerate(text):
        if i+1 in [9,14,19,24]:
          if char == '-':
            fontColour = 'black'
          else:
            fontColour = 'red'
        else:
          fontColour = 'black' if char in '0123456789abcdef' else 'red'
        if i > 35: # too many chars
          bgColour = 'yellow'
        elif len(text) < 36: # Not enough chars
          bgColour = 'yellow'
        else: # standard case
          bgColour = 'white'
        widgets.append(tk.Label(frame, text=char, fg=fontColour, bg=bgColour, font=('Arial', 12), width=0))
        widgets[-1].grid(row=row, column=i+1, padx=0)
    widgets.append(tk.Button(frame, text="Copy", command=func))
    widgets[-1].grid(row=row, column=i+2, padx=0)
    print(text)

def add_to_clipboard(text):
    pyperclip.copy(text)
    # the below fails with this error even though pywin32 is already installed
    # ModuleNotFoundError: No module named 'win32api'
    #toaster = ToastNotifier()
    #toaster.show_toast("GUID OCR", f"{text} has been added to your clipboard", duration=2)

def copyfixed():
    add_to_clipboard(fixed)
    root.destroy()

def copyoriginal():
    add_to_clipboard(extracted_text)
    root.destroy()

def close_on_escape(event=None):
    root.destroy()

parser = argparse.ArgumentParser(description="")
parser.add_argument(
    '--clipboard',
    action='store_true',
    help='Use clipboard input'
)
parser.add_argument(
    '--path',
    type=str,
    help='Specify the file path'
)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.clipboard:
        image = ImageGrab.grabclipboard()
    elif args.path == 'recent':
        pathdir = os.sep.join([os.path.expanduser('~'),r'Pictures\Screenshots'])
        lastscreenshot = os.sep.join([pathdir,sorted([i for i in os.listdir(pathdir) if '.png' in i.lower()])[-1]])
        image = PIL.Image.open(lastscreenshot)
    elif args.path:
        image = PIL.Image.open(args.path)
    else:
        print("No Picture chosen")
    try:
        extracted_text = pytesseract.image_to_string(image).strip()#.lower()
    except pytesseract.pytesseract.TesseractNotFoundError as e:
        print(e)
        print(f"""You must install tesseract and add it to your path
        https://github.com/UB-Mannheim/tesseract/wiki
        """)
        
    #extracted_text = '3aacf3ac-2d46-47d8-b021-630bbde24b42'
    if len(extracted_text) > 40:
        print('Invalid image script not run')
    else:        
        root = tk.Tk()
        root.withdraw()
        # Get mouse loc
        x = root.winfo_pointerx()-300
        y = root.winfo_pointery()-50
        top = tk.Toplevel(root)
        top.geometry(f"+{x}+{y}")  
        
        top.title("OCR Result")
        top.attributes("-topmost", True)
        top.bind("<Escape>", close_on_escape)

        widgets = []

        frame = tk.Frame(top)
        frame.pack(padx=3, pady=3)
        widgets.append(tk.Label(frame, text="First pass:", fg='black', font=('Arial', 16), width=0))
        widgets[-1].grid(row=0, column=0, padx=2)
        # Display each character as a label
        validate_text(extracted_text, copyoriginal, 0)
        fixed = fix(extracted_text)
        add_to_clipboard(fixed)

        if fixed != extracted_text:
            widgets.append(tk.Label(frame, text="Fixed:", fg='black', font=('Arial', 16), width=0))
            widgets[-1].grid(row=1, column=0, padx=2)
            validate_text(fixed, copyfixed, row=1)
        root.mainloop()
