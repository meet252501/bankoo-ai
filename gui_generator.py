"""
Bankoo AI - Natural Language GUI Generator
Generates and launches GUI applications from text descriptions
"""

import subprocess
import tempfile
import os

# GUI Templates
GUI_TEMPLATES = {
    "calculator": '''import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())
        result_label.config(text=f"Result: {result}")
    except:
        result_label.config(text="Error!")

root = tk.Tk()
root.title("Bankoo Calculator")
root.geometry("350x250")

tk.Label(root, text="Enter Expression:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, width=30, font=("Arial", 14))
entry.pack(pady=10)

tk.Button(root, text="Calculate", command=calculate, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

result_label = tk.Label(root, text="Result: ", font=("Arial", 16), fg="blue")
result_label.pack(pady=10)

root.mainloop()
''',
    
    "todo": '''import tkinter as tk

def add_task():
    task = entry.get()
    if task:
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)

def delete_task():
    try:
        listbox.delete(listbox.curselection())
    except:
        pass

root = tk.Tk()
root.title("Bankoo To-Do List")
root.geometry("400x400")

tk.Label(root, text="To-Do List", font=("Arial", 18, "bold")).pack(pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=10)

tk.Button(root, text="Add Task", command=add_task, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_task, bg="#f44336", fg="white").pack(pady=5)

listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 11))
listbox.pack(pady=10)

root.mainloop()
''',
    
    "clock": '''import tkinter as tk
import time

def update_time():
    current_time = time.strftime("%H:%M:%S")
    label.config(text=current_time)
    root.after(1000, update_time)

root = tk.Tk()
root.title("Bankoo Clock")
root.geometry("300x150")

label = tk.Label(root, font=("Arial", 40, "bold"), fg="blue")
label.pack(expand=True)

update_time()
root.mainloop()
''',

    "notepad": '''import tkinter as tk
from tkinter import filedialog

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(text.get("1.0", tk.END))

root = tk.Tk()
root.title("Bankoo Notepad")
root.geometry("600x400")

text = tk.Text(root, font=("Arial", 12), wrap=tk.WORD)
text.pack(expand=True, fill=tk.BOTH)

tk.Button(root, text="Save File", command=save_file, bg="#4CAF50", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
'''
}

def create_gui(app_type="calculator"):
    """
    Creates and launches a GUI application
    app_type: 'calculator', 'todo', 'clock', 'notepad'
    """
    if app_type not in GUI_TEMPLATES:
        print(f"Unknown app type: {app_type}")
        print(f"Available: {', '.join(GUI_TEMPLATES.keys())}")
        return
    
    code = GUI_TEMPLATES[app_type]
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
    temp_file.write(code)
    temp_file.close()
    
    # Launch
    print(f"Launching {app_type}...")
    subprocess.Popen(['python', temp_file.name])
    print(f"GUI launched! Check your taskbar.")

if __name__ == "__main__":
    import sys
    
    print("Bankoo AI - Natural Language GUI Generator")
    print("=" * 50)
    print("Available apps:")
    for app in GUI_TEMPLATES.keys():
        print(f"  - {app}")
    print()
    
    if len(sys.argv) > 1:
        create_gui(sys.argv[1])
    else:
        app = input("Enter app name (or press Enter for calculator): ").strip().lower()
        if not app:
            app = "calculator"
        create_gui(app)
