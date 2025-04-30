import tkinter as tk
from tkinter import ttk

# System Vars
version = "4.0.0"
options = [
    "Add lists",
    "Delete lists",
    "View and Modify Lists"
]

# Tkinter Variables
root = tk.Tk()
root.title(f"ToDoList {version}")
winW = 450
winH = 250

def center_screen():
    screenW = root.winfo_screenwidth()
    screenH = root.winfo_screenheight()
    centerX = int(screenW/2 - winW / 2)
    centerY = int(screenH/2 - winH / 2)

    root.geometry(f"{winW}x{winH}+{centerX}+{centerY}")
    root.resizable(False, False)
center_screen()

def on_select(event):
    AddList()
    DeleteList()  
    View_ModifyLists()

optionDropdown = ttk.Combobox(root, values=options)
optionDropdown.current(2)
optionDropdown.pack(anchor=tk.N)
optionDropdown.bind("<<ComboboxSelected>>", on_select)

VMLtempLabel = ttk.Label(root, text="This feature is being developed: View and Modify Lists")
ALtempLabel = ttk.Label(root, text="This feature is being developed: Add Lists")
DLtempLabel = ttk.Label(root, text="This feature is being developed: Delete Lists")

def AddList():
    if optionDropdown.get() == "Add lists":
        ALtempLabel.pack(anchor=tk.N)
    else:
        ALtempLabel.pack_forget()

def DeleteList():
    if optionDropdown.get() == "Delete lists":
        DLtempLabel.pack(anchor=tk.N)
    else:
        DLtempLabel.pack_forget()

def View_ModifyLists():
    if optionDropdown.get() == "View and Modify Lists":
        VMLtempLabel.pack(anchor=tk.N)
    else:
        VMLtempLabel.pack_forget()


def main():
    AddList()
    DeleteList()
    View_ModifyLists()
    root.mainloop()

if __name__ == '__main__':
    main()