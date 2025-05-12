import tkinter as tk
from tkinter import ttk

### SYSTEM VARIABLES ###

version = "4.0.0"
options = [
    "Add lists",
    "Delete lists",
    "View and Modify Lists"
]
todo = {}
lists = []

# Tkinter Variables
root = tk.Tk()
root.title(f"ToDoList {version}")
winW = 450
winH = 400
btn_padding = 10

### Visible function variables
addtaskvisible = 0
addlistvisible = 0
button_frame = tk.Frame(root)


# Center Screen Function
def center_screen():
    screenW = root.winfo_screenwidth()
    screenH = root.winfo_screenheight()
    centerX = int(screenW/2 - winW / 2)
    centerY = int(screenH/2 - winH / 2)

    root.geometry(f"{winW}x{winH}+{centerX}+{centerY}")
    root.resizable(False, False)
center_screen()

### LOGIC FUNCTIONS ###

# Rendering Individual screens whenever an option on the Dropdown is clicked
def on_select(event):
    AddListWidget()
    DeleteListWidget()  
    View_ModifyListsWidget()

# Addlist Function for AddListWidget()
def AddList():
    new_todo = {}
    listname = addlist_entry.get()
    todo[listname] = new_todo
    lists.append(listname)
    addlist_confirmation_var.set(f"New list created with the title {listname}")
    update_lists_dropdown()

def update_lists_dropdown():
    listsDropdown['values'] = lists
    display_List()

def display_List():
    listDisplay.delete(1.0, tk.END)
    current_list_name = listsDropdown.get()
    if current_list_name in todo:
        for key, value in todo[current_list_name].items():
            listDisplay.insert(tk.END, f"{key}: {value}\n")  

def AddTask():
    is_completed = "X"
    item_name = addtask_entry.get()
    listLookup = listsDropdown.get()

    todo[listLookup].update({item_name: is_completed})
    f"Updated list: {todo[listLookup]}"
    display_List()

def CompleteTask():
    pass

def ShowAddTask():
    global addtaskvisible
    if optionDropdown.get() == "View and Modify Lists":
        if addtaskvisible == 0:
            addtask_entry.pack(pady=10, padx=10)
            comfirm_new_task.pack(pady=5)
            addtaskvisible = 1
        else:
            addtask_entry.pack_forget()
            comfirm_new_task.pack_forget()
            addtaskvisible = 0
    elif optionDropdown.get() != "View and Modify Lists":
        addtask_entry.pack_forget()
        comfirm_new_task.pack_forget()
        addtaskvisible = 0

### DISPLAY WIDGETS ###

### Dropdown
optionDropdown = ttk.Combobox(root, values=options, justify=tk.CENTER)
optionDropdown.current(2)
optionDropdown.pack(anchor=tk.N)
optionDropdown.bind("<<ComboboxSelected>>", on_select)

### Temporary Widgets
DLtempLabel = ttk.Label(root, text="This feature is being developed: Delete Lists")

### View_ModifyListsWidget() Widgets
currentList = tk.StringVar()
listsDropdown = ttk.Combobox(root, values=lists, justify=tk.CENTER)
listDisplay = tk.Text(root, height=10)
### AddTask() Widgets
new_task = tk.StringVar()
addtask_btn = ttk.Button(root, text="Add Task", command=ShowAddTask)
addtask_entry = ttk.Entry(root, textvariable=new_task)
comfirm_new_task = ttk.Button(root, text="Confirm", command=AddTask)
### DeleteTask() Widgets
delete_task = tk.StringVar()
delete_task_btn = ttk.Button(root, text="Delete Task")
delete_task_entry = ttk.Entry(root, textvariable=delete_task)
delete_task_label = tk.Label(root, text="Delete Task")
### AddList() Widgets
new_list = tk.StringVar()
addlist_btn = ttk.Button(root, text="Add List")
addlist_confirmation_var = tk.StringVar()
addlist_entry = tk.Entry(root, textvariable=new_list)
addlist_label = tk.Label(root, text="New List")
addlist_button = tk.Button(root, text="Add List", command=AddList)
addlist_comfirmation = tk.Label(root, textvariable=addlist_confirmation_var)
### DeleteList() Widgets
delete_list = tk.StringVar()
delete_list_btn = ttk.Button(root, text="Delete List")
delete_list_entry = ttk.Entry(root, textvariable=delete_list)
delete_list_label = tk.Label(root, text="Delete List")
delete_list_button = tk.Button(root, text="Delete List")


# Add List Function
def AddListWidget():
    if optionDropdown.get() == "Add lists":
        addlist_label.pack(anchor=tk.N)
        addlist_entry.pack(anchor=tk.N)
        addlist_button.pack(anchor=tk.N, pady=10)
        addlist_comfirmation.pack(anchor=tk.N, pady=30)

    else:
        addlist_label.pack_forget()
        addlist_entry.pack_forget()
        addlist_button.pack_forget()
        addlist_comfirmation.pack_forget()
        

def DeleteListWidget():
    if optionDropdown.get() == "Delete lists":
        DLtempLabel.pack(anchor=tk.N)
    else:
        DLtempLabel.pack_forget()

def View_ModifyListsWidget():
    if optionDropdown.get() == "View and Modify Lists":
        listsDropdown.pack(anchor=tk.N, pady=10)
        listDisplay.pack(anchor=tk.W, padx=20, pady=10)
        addtask_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
        delete_task_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
        addlist_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
        delete_list_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
        button_frame.pack(anchor=tk.SW, pady=15, padx=15)
        ShowAddTask()
    else:
        listsDropdown.pack_forget()
        listDisplay.pack_forget()
        addtask_btn.pack_forget()


def main():
    update_lists_dropdown()
    AddListWidget()
    DeleteListWidget()
    View_ModifyListsWidget()
    ShowAddTask()
    root.mainloop()

if __name__ == '__main__':
    main()