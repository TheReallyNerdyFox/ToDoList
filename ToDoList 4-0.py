import tkinter as tk
from tkinter import ttk
import json


### SYSTEM VARIABLES ###

version = "4.0.0"
options = [
    "Add lists",
    "Delete lists",
    "View and Modify Lists"
]
todo = {}
lists = []

# Saving and Loading defs
def save_data():
    data = {
        "todo": todo,   
        "lists": lists 
    }
    
    with open("todo_data.json", "w") as file:
        json.dump(data, file, indent=4)
        print("Data saved successfully.")

# Load todo and lists data from a JSON file
def load_data():
    global todo, lists
    try:
        with open("todo_data.json", "r") as file:
            data = json.load(file)
            todo = data.get("todo", {})
            lists = data.get("lists", [])
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("No previous data found. Starting fresh.")

# Tkinter Variables
root = tk.Tk()
root.title(f"ToDoList {version}")
winW = 475
winH = 500
btn_padding = 10

### Visible function variables
addtaskvisible = 0
addlistvisible = 0
deltaskvisible = 0
dellistvisible = 0
button_frame = tk.Frame(root)
save_load_frame = tk.Frame(root)

### SPAGHETTI ###

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

def on_select(event):
    update_lists_dropdown()
    display_List()

# Addlist() logic
def AddList():
    new_todo = {}
    listname = addlist_entry.get()
    todo[listname] = new_todo
    lists.append(listname)
    addlist_confirmation_var.set(f"New list created with the title {listname}")
    update_lists_dropdown()
    save_data()

def update_lists_dropdown():
    listsDropdown['values'] = lists
    if lists:
        listsDropdown.set(lists[0])
    else:
        listsDropdown.set("")
    display_List()

def remove_list():
    list_name = listsDropdown.get()
    
    if list_name in todo:
        del todo[list_name]
        lists.remove(list_name)

        update_lists_dropdown()
        
        if len(lists) == 0:
            listsDropdown.set("")
    else:
        pass

def display_List():
    for widget in listDisplay.winfo_children():
        widget.destroy()

    current_list_name = listsDropdown.get()
    if current_list_name in todo:
        for task, is_completed in todo[current_list_name].items():
            var = tk.BooleanVar(value=(is_completed == "✔"))
            checkbox = tk.Checkbutton(listDisplay, text=task, variable=var, 
                                      command=lambda t=task, v=var: toggle_task(current_list_name, t, v))
            checkbox.pack(anchor=tk.W)

def toggle_task(list_name, task, var):
    todo[list_name][task] = "✔" if var.get() else "X"

def remove_task():
    list_name = listsDropdown.get()
    task_to_delete = delete_task_dropdown.get()

    if list_name in todo and task_to_delete in todo[list_name]:
        todo[list_name].pop(task_to_delete, None)

    update_delete_dropdown()
    display_List()
    delete_task_dropdown.set("")

def update_delete_dropdown():
    current_list_name = listsDropdown.get()

    if current_list_name in todo:
        delete_task_dropdown['values'] = list(todo[current_list_name].keys())
    else:
        delete_task_dropdown['values'] = []
    

def AddTask():
    is_completed = "X"
    item_name = addtask_entry.get()
    listLookup = listsDropdown.get()
    newtaskLabel.set(f"New task created with the title {item_name}")
    todo[listLookup].update({item_name: is_completed})
    display_List()

def ShowAddTask():
    global dellistvisible, deltaskvisible, addtaskvisible, addlistvisible      
    if addtaskvisible == 0:
        if addlistvisible == 1:
            ShowAddList()
        if deltaskvisible == 1:
            ShowDelTask()
        if dellistvisible == 1:
            ShowDelList()

        addtask_label.pack(anchor=tk.N)
        addtask_entry.pack(pady=10, padx=10)
        comfirm_new_task.pack(pady=5)
        addtask_confirmation.pack(pady=5)
        addtaskvisible = 1
    else:
        addtask_label.pack_forget()
        newtaskLabel.set("")
        addtask_entry.delete(0, tk.END)
        addtask_entry.pack_forget()
        comfirm_new_task.pack_forget()
        addtask_confirmation.pack_forget()
        addtaskvisible = 0

def ShowAddList():
    global dellistvisible, deltaskvisible, addtaskvisible, addlistvisible

    if addlistvisible == 0:
        if addtaskvisible == 1:
            ShowAddTask()
        if deltaskvisible == 1:
            ShowDelTask()
        if dellistvisible == 1:
            ShowDelList()

        addlist_label.pack(anchor=tk.N)
        addlist_entry.pack(anchor=tk.N, padx=10, pady=10)
        addlist_button.pack(anchor=tk.N, pady=5)
        addlist_comfirmation.pack(anchor=tk.N, pady=5)
        addlistvisible = 1
    else:
        addlist_confirmation_var.set("")
        addlist_entry.delete(0, tk.END)
        addlist_label.pack_forget()
        addlist_entry.pack_forget()
        addlist_button.pack_forget()
        addlist_comfirmation.pack_forget()
        addlistvisible = 0

def ShowDelTask():
    global dellistvisible, deltaskvisible, addtaskvisible, addlistvisible

    if deltaskvisible == 0:
        if addlistvisible == 1:
            ShowAddList()
        if addtaskvisible == 1:
            ShowAddTask()
        if dellistvisible == 1:
            ShowDelList()

        update_delete_dropdown()

        delete_task_label.pack(anchor=tk.N)
        delete_task_dropdown.pack(anchor=tk.N, padx=10, pady=10)
        confirm_delete_task.pack(anchor=tk.N, pady=5)
        deltaskvisible = 1
    else:
        delete_task_label.pack_forget()
        delete_task_dropdown.pack_forget()
        confirm_delete_task.pack_forget()
        deltaskvisible = 0

def ShowDelList():
    global dellistvisible, deltaskvisible, addtaskvisible, addlistvisible

    if dellistvisible == 0:
        if addlistvisible == 1:
            ShowAddList()
        if addtaskvisible == 1:
            ShowAddTask()
        if deltaskvisible == 1:
            ShowDelTask()
        
        delete_list_label.pack(anchor=tk.N)
        delete_list_info_label.pack(anchor=tk.N, padx=10, pady=10)
        delete_list_button.pack(anchor=tk.N, pady=5)
        dellistvisible = 1
    else:
        delete_list_label.pack_forget()
        delete_list_info_label.pack_forget()
        delete_list_button.pack_forget()
        dellistvisible = 0

### DISPLAY WIDGETS ###

### View_ModifyListsWidget() Widgets
currentList = tk.StringVar()
listsDropdown = ttk.Combobox(root, values=lists, justify=tk.CENTER)
listsDropdown.bind('<<ComboboxSelected>>', on_select)
listDisplay = tk.Frame(root, width=400, height=175)
save_btn = ttk.Button(root, text="Save Lists", command=save_data)
load_btn = ttk.Button(root, text="Load Lists", command=load_data)

### AddTask() Widgets
new_task = tk.StringVar()
newtaskLabel = tk.StringVar()
addtask_label = tk.Label(root, text="Add Task")
addtask_btn = ttk.Button(root, text="Add Task", command=ShowAddTask)
addtask_entry = ttk.Entry(root, textvariable=new_task)
comfirm_new_task = ttk.Button(root, text="Confirm", command=AddTask)
addtask_confirmation = tk.Label(root, textvariable=newtaskLabel)

### DeleteTask() Widgets
delete_task = tk.StringVar()
delete_task_btn = ttk.Button(root, text="Delete Task", command=ShowDelTask)
delete_task_label = ttk.Label(root, text="Delete Task")
delete_task_dropdown = ttk.Combobox(root, values=[], justify=tk.CENTER)
confirm_delete_task = ttk.Button(root, text="Confirm", command=remove_task)

### AddList() Widgets
new_list = tk.StringVar()
addlist_btn = ttk.Button(root, text="Add List", command=ShowAddList)
addlist_confirmation_var = tk.StringVar()
addlist_entry = tk.Entry(root, textvariable=new_list)
addlist_label = tk.Label(root, text="Add List")
addlist_button = tk.Button(root, text="Confirm", command=AddList)
addlist_comfirmation = tk.Label(root, textvariable=addlist_confirmation_var)

### DeleteList() Widgets
delete_list = tk.StringVar()
delete_list_btn = ttk.Button(root, text="Delete List", command=ShowDelList)
delete_list_label = tk.Label(root, text="Delete List")
delete_list_info_label = tk.Label(root, text="This will delete the current list.")
delete_list_button = tk.Button(root, text="Delete List", command=remove_list)

def View_ModifyListsWidget():
    listsDropdown.pack(anchor=tk.N, pady=10)
    listDisplay.pack_propagate(False)
    listDisplay.pack(anchor=tk.W, padx=20, pady=10)
    addtask_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
    delete_task_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
    addlist_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
    delete_list_btn.pack(in_=button_frame, side=tk.LEFT, padx=btn_padding)
    button_frame.pack(anchor=tk.SW, pady=15, padx=15)
    save_btn.pack(in_=save_load_frame, side=tk.LEFT)
    load_btn.pack(in_=save_load_frame, side=tk.LEFT)
    save_load_frame.pack(side=tk.BOTTOM, pady=20)
    ShowAddTask()


def main():
    load_data()
    update_lists_dropdown()
    View_ModifyListsWidget()
    ShowAddTask()
    root.mainloop()

if __name__ == '__main__':
    main()