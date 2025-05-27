#! /usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
import threading
import time

version = "4.1.0"


class ToDoApp:
    def __init__(self, root: tk.Tk):
        """
        Constructor for the ToDoApp class. Responsible for initializing GUI and setting up necessary data structures.
        Parameters:
        root (tk.Tk): The root window of the application
        """
        # setting up the root window (note: initializes to fullscreen)
        self.root = root
        self.root.title(f"ToDo List v{version}")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

        # loads all the users and logs in
        self.users = self.load_users()
        self.current_user = None
        self.login()

        # load the application data
        self.data = self.load_data()
        self.lists = self.data.get("lists", [])
        self.tasks = self.data.get("todo", {})

        # create some variables to track stuff
        self.current_list = tk.StringVar()
        self.current_list.trace_add("write", self.refresh)
        self.detail_vars = {
            "due_date": tk.StringVar(),
            "reminder": tk.StringVar(),
            "progress": tk.IntVar(),
            "notes": tk.StringVar(),
            "tags": tk.StringVar(),
            "attachment": tk.StringVar(),
            "priority": tk.StringVar(),
            "assignee": tk.StringVar(),
        }

        # show the user all the hard work we just did
        self.create_widgets()
        self.update_lists_dropdown()
        self.center_screen()

        # start the reminder thread
        self.reminder_thread = threading.Thread(target=self.check_reminders)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)

        tk.Label(top_frame, text="Select List:").pack(side=tk.LEFT, padx=5)
        self.lists_dropdown = ttk.Combobox(
            top_frame, textvariable=self.current_list, state="readonly"
        )
        self.lists_dropdown.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side=tk.RIGHT, padx=5)

        actions = [
            ("Add List", self.show_add_list),
            ("Delete List", self.delete_list),
            ("Edit List", self.show_edit_list),
            ("Save", self.save_data),
            ("Login", self.login),
            ("Register", self.register),
        ]

        for txt, cmd in actions:
            tk.Button(btn_frame, text=txt, command=cmd).pack(side=tk.LEFT, padx=2)

        self.task_frame = tk.LabelFrame(self.root, text="Tasks")
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tasks_canvas = tk.Canvas(self.task_frame)
        self.tasks_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll = tk.Scrollbar(
            self.task_frame, orient="vertical", command=self.tasks_canvas.yview
        )
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_canvas.configure(yscrollcommand=scroll.set)

        self.tasks_inner = tk.Frame(self.tasks_canvas)
        self.tasks_canvas.create_window((0, 0), window=self.tasks_inner, anchor="nw")

        self.tasks_inner.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(
                scrollregion=self.tasks_canvas.bbox("all")
            ),
        )

        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=5, fill=tk.X)

        self.task_entry = tk.Entry(input_frame)
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        task_actions = [
            ("Add Task", self.add_task),
            ("Edit Task", self.show_edit_task),
            ("Delete Task", self.show_delete_task),
        ]

        for txt, cmd in task_actions:
            tk.Button(input_frame, text=txt, command=cmd).pack(side=tk.LEFT, padx=5)

        adv_frame = tk.LabelFrame(self.root, text="Advanced Features")
        adv_frame.pack(fill=tk.X, padx=10, pady=5)

        adv_actions = [
            ("Move Task", self.show_move_task),
            ("Sort Tasks", self.sort_tasks),
            ("Filter Tasks", self.show_filter),
            ("Export Tasks", self.export_tasks),
            ("Import Tasks", self.import_tasks),
            ("Search", self.show_search),
        ]

        for txt, cmd in adv_actions:
            tk.Button(adv_frame, text=txt, command=cmd).pack(
                side=tk.LEFT, padx=3, pady=3
            )

        self.details_frame = tk.LabelFrame(self.root, text="Task Details")
        self.details_frame.pack(fill=tk.X, padx=10, pady=5)

        labels = [
            "Due Date (YYYY-MM-DD):",
            "Reminder (HH:MM)",
            "Progress (%):",
            "Notes:",
            "Tags (comma separated):",
            "Attachment Path:",
            "Priority:",
            "Assignee:",
        ]

        for i, label in enumerate(labels):
            tk.Label(self.details_frame, text=label).grid(row=i, column=0, sticky=tk.W)

        self.due_date_entry = tk.Entry(
            self.details_frame, textvariable=self.detail_vars["due_date"]
        )
        self.due_date_entry.grid(row=0, column=1, sticky=tk.EW)

        self.reminder_entry = tk.Entry(
            self.details_frame, textvariable=self.detail_vars["reminder"]
        )
        self.reminder_entry.grid(row=1, column=1, sticky=tk.EW)

        self.progress_scale = tk.Scale(
            self.details_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.detail_vars["progress"],
        )
        self.progress_scale.grid(row=2, column=1, sticky=tk.EW)

        self.notes_entry = tk.Entry(
            self.details_frame, textvariable=self.detail_vars["notes"]
        )
        self.notes_entry.grid(row=3, column=1, sticky=tk.EW)

        self.tags_entry = tk.Entry(
            self.details_frame, textvariable=self.detail_vars["tags"]
        )
        self.tags_entry.grid(row=4, column=1, sticky=tk.EW)

        self.attachment_label = tk.Label(
            self.details_frame, textvariable=self.detail_vars["attachment"]
        )
        self.attachment_label.grid(row=5, column=1, sticky=tk.EW)

        self.attach_btn = tk.Button(
            self.details_frame, text="Attach File", command=self.attach_file
        )
        self.attach_btn.grid(row=5, column=2, sticky=tk.W)

        self.priority_var = tk.StringVar()
        self.priority_var.set("Low")
        self.priority_menu = ttk.OptionMenu(
            self.details_frame, self.priority_var, "Low", "Medium", "High"
        )
        self.priority_menu.grid(row=6, column=1, sticky=tk.EW)

        self.assignee_var = tk.StringVar()
        self.assignee_var.set(next(iter(self.users or {"": ""})))
        self.assignee_menu = ttk.OptionMenu(
            self.details_frame, self.assignee_var, *self.users.keys()
        )
        self.assignee_menu.grid(row=7, column=1, sticky=tk.EW)

        self.details_frame.grid_columnconfigure(1, weight=1)

        tk.Button(
            self.details_frame, text="Save Details", command=self.save_task_details
        ).grid(row=8, column=0, columnspan=3, pady=5)

    def login(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Login")
        dialog.geometry("550x400")

        tk.Label(dialog, text="Username:").pack(padx=10, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.pack(padx=10, pady=5)

        tk.Label(dialog, text="Password:").pack(padx=10, pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack(padx=10, pady=5)

        def login2():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.users and self.users[username] == password:
                self.current_user = username
                dialog.destroy()
            else:
                messagebox.showerror("Invalid credentials", "Please try again.")

        tk.Button(dialog, text="Login", command=login2).pack(pady=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                return json.load(f)
        else:
            return {}

    def save_users(self):
        with open("users.json", "w") as f:
            json.dump(self.users, f)

    def register(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Register")
        dialog.geometry("550x400")

        tk.Label(dialog, text="Username:").pack(padx=10, pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.pack(padx=10, pady=5)

        tk.Label(dialog, text="Password:").pack(padx=10, pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack(padx=10, pady=5)

        def register2():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.users:
                messagebox.showerror(
                    "Username exists", "Please choose a different username."
                )
                return
            self.users[username] = password
            self.save_users()
            messagebox.showinfo("Registered", "You have been registered successfully.")
            dialog.destroy()

        tk.Button(dialog, text="Register", command=register2).pack(pady=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def load_data(self):
        if os.path.exists("todo_data.json"):
            with open("todo_data.json", "r") as f:
                return json.load(f)
        else:
            return {"lists": [], "todo": {}}

    def save_data(self):
        with open("todo_data.json", "w") as f:
            json.dump({"lists": self.lists, "todo": self.tasks}, f)

    def refresh(self, *args):
        # the *args are here so it can be called by tkinter callback, we ignore the extras
        self.update_lists_dropdown(refresh_tasks=False)
        self.refresh_task_display()

    def update_lists_dropdown(self, refresh_tasks=True):
        self.lists_dropdown["values"] = self.lists
        if self.lists and self.current_list.get() not in self.lists:
            self.current_list.set(self.lists[0])
        elif not self.lists:
            self.current_list.set("")
        if refresh_tasks:
            self.refresh_task_display()

    def refresh_task_display(self):
        for w in self.tasks_inner.winfo_children():
            w.destroy()
        self.selected_task = None
        lst = self.current_list.get()
        if not lst or lst not in self.tasks:
            return
        for task, meta in self.tasks[lst].items():
            var = tk.BooleanVar(value=meta.get("completed", False))
            cb = tk.Checkbutton(
                self.tasks_inner,
                text=task,
                variable=var,
                command=lambda t=task, v=var: self.toggle_completion(t, v),
            )
            cb.pack(anchor=tk.W, fill=tk.X, padx=5, pady=2)
            cb.bind("<Button-3>", lambda e, t=task: self.select_task(e, t))

    def toggle_completion(self, task, var):
        lst = self.current_list.get()
        if lst in self.tasks and task in self.tasks[lst]:
            self.tasks[lst][task]["completed"] = var.get()
            self.save_data()

    def select_task(self, event, task):
        lst = self.current_list.get()
        if lst in self.tasks and task in self.tasks[lst]:
            self.selected_task = task
            meta = self.tasks[lst][task]
            for key, var in self.detail_vars.items():
                val = meta.get(key, "")
                if key == "tags" and isinstance(val, list):
                    val = ",".join(val)
                elif key == "progress":
                    val = val or 0
                var.set(val)
            messagebox.showinfo(
                "Task Selected", f"Selected task '{task}'. Edit details below."
            )

    def attach_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.detail_vars["attachment"].set(file)
            filename = os.path.basename(file)
            if not os.path.exists("attachments"):
                os.makedirs("attachments")
            attachment_path = os.path.join("attachments", filename)
            with open(file, "rb") as f:
                with open(attachment_path, "wb") as f2:
                    f2.write(f.read())
            self.detail_vars["attachment"].set(attachment_path)

    def save_task_details(self):
        task = self.selected_task
        lst = self.current_list.get()
        if not task or lst not in self.tasks or task not in self.tasks[lst]:
            messagebox.showwarning(
                "No task selected", "Select a task by right-clicking it."
            )
            return
        # Validate dates
        dd = self.detail_vars["due_date"].get().strip()
        rem = self.detail_vars["reminder"].get().strip()
        if dd:
            try:
                datetime.strptime(dd, "%Y-%m-%d")
            except:
                return messagebox.showerror(
                    "Invalid date", "Due Date format must be YYYY-MM-DD"
                )
        if rem:
            try:
                datetime.strptime(rem, "%H:%M")
            except:
                return messagebox.showerror(
                    "Invalid time", "Reminder format must be HH:MM"
                )
        # Save metadata
        meta = self.tasks[lst][task]
        meta["due_date"] = dd
        meta["reminder"] = rem
        meta["progress"] = self.detail_vars["progress"].get()
        meta["notes"] = self.detail_vars["notes"].get().strip()
        meta["tags"] = [
            t.strip() for t in self.detail_vars["tags"].get().split(",") if t.strip()
        ]
        meta["attachment"] = self.detail_vars["attachment"].get().strip()
        meta["priority"] = self.priority_var.get()
        meta["assignee"] = self.assignee_var.get()
        self.save_data()
        messagebox.showinfo("Saved", f"Details saved for task '{task}'.")

    def add_task(self):
        lst = self.current_list.get()
        if not lst:
            return messagebox.showwarning("No list", "Select or add a list first.")
        t = self.task_entry.get().strip()
        if not t:
            return messagebox.showwarning("No task", "Enter a task name.")
        if t in self.tasks.get(lst, {}):
            return messagebox.showwarning("Duplicate task", "Task already exists.")
        self.tasks.setdefault(lst, {})[t] = {
            "completed": False,
            "due_date": "",
            "reminder": "",
            "progress": 0,
            "notes": "",
            "tags": [],
            "attachment": "",
            "priority": "Low",
            "assignee": next(iter(self.users or {"": ""})),
        }
        self.task_entry.delete(0, tk.END)
        self.save_data()
        self.refresh_task_display()

    def delete_list(self):
        lst = self.current_list.get()
        if not lst:
            return
        if messagebox.askyesno("Confirm", f"Delete list '{lst}'?"):
            self.tasks.pop(lst, None)
            if lst in self.lists:
                self.lists.remove(lst)
            self.save_data()
            self.update_lists_dropdown()

    def show_add_list(self):
        self.popup_simple("Add List", "List Name:", self.add_list)

    def add_list(self, name):
        name = name.strip()
        if not name or name in self.lists:
            messagebox.showwarning("Invalid name", "Enter unique non-empty list name.")
            return False
        self.lists.append(name)
        self.tasks[name] = {}
        self.save_data()
        self.update_lists_dropdown()
        self.current_list.set(name)
        return True

    def popup_simple(self, title, label, on_confirm):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("550x400")

        tk.Label(dialog, text=label).pack(padx=10, pady=5)
        entry = tk.Entry(dialog)
        entry.pack(padx=10, pady=5)
        entry.focus_set()

        def confirm():
            if on_confirm(entry.get()):
                dialog.destroy()

        tk.Button(dialog, text="Confirm", command=confirm).pack(pady=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def show_edit_list(self):
        lst = self.current_list.get()
        if not lst:
            return messagebox.showwarning("No list", "Select list first.")

        def on_confirm(new_name):
            new_name = new_name.strip()
            if not new_name or (new_name != lst and new_name in self.lists):
                messagebox.showwarning("Invalid", "Unique non-empty name required.")
                return False
            self.tasks[new_name] = self.tasks.pop(lst)
            self.lists[self.lists.index(lst)] = new_name
            self.current_list.set(new_name)
            self.save_data()
            self.update_lists_dropdown()
            return True

        self.popup_simple("Edit List", "New name:", on_confirm)

    def show_edit_task(self):
        lst = self.current_list.get()
        if not lst or not self.tasks.get(lst):
            return messagebox.showwarning("No tasks", "No tasks in current list.")

        self.popup_task_edit(lst)

    def popup_task_edit(self, list_name):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("500x400")

        tk.Label(dialog, text="Select Task:").pack(pady=5)
        task_var = tk.StringVar()
        tasks = list(self.tasks[list_name].keys())
        dropdown = ttk.Combobox(
            dialog, values=tasks, textvariable=task_var, state="readonly"
        )
        dropdown.pack(pady=5)
        dropdown.current(0)

        tk.Label(dialog, text="New Name:").pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def save():
            old = task_var.get()
            new = entry.get().strip()
            if not new:
                messagebox.showwarning("Invalid", "Enter name.")
                return
            if new != old and new in self.tasks[list_name]:
                messagebox.showwarning("Duplicate", "Task name exists.")
                return
            self.tasks[list_name][new] = self.tasks[list_name].pop(old)
            self.save_data()
            self.refresh_task_display()
            dialog.destroy()

        tk.Button(dialog, text="Save", command=save).pack(pady=10)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def show_delete_task(self):
        lst = self.current_list.get()
        if not lst or not self.tasks.get(lst):
            return messagebox.showwarning("No tasks", "No tasks in current list.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Task")
        dialog.geometry("550x400")

        tk.Label(dialog, text="Select Task:").pack(pady=5)
        task_var = tk.StringVar()
        tasks = list(self.tasks[lst].keys())
        dropdown = ttk.Combobox(
            dialog, values=tasks, textvariable=task_var, state="readonly"
        )
        dropdown.pack(pady=5)
        dropdown.current(0)

        def delete():
            task = task_var.get()
            if messagebox.askyesno("Confirm", f"Delete task '{task}'?"):
                self.tasks[lst].pop(task)
                self.save_data()
                self.refresh_task_display()
                dialog.destroy()

            tk.Button(dialog, text="Delete", command=delete).pack(pady=10)

            dialog.transient(self.root)
            dialog.grab_set()
            self.root.wait_window(dialog)

    def show_move_task(self):
        lst = self.current_list.get()
        if not lst or not self.tasks.get(lst):
            return messagebox.showwarning("No tasks", "No tasks in current list.")
        if len(self.lists) < 2:
            return messagebox.showinfo("No Lists", "Add more lists to move tasks.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Move Task")
        dialog.geometry("550x400")

        tk.Label(dialog, text="Select Task:").pack(pady=5)
        task_var = tk.StringVar()
        tasks = list(self.tasks[lst].keys())
        task_dropdown = ttk.Combobox(
            dialog, values=tasks, textvariable=task_var, state="readonly"
        )
        task_dropdown.pack(pady=5)
        task_dropdown.current(0)

        tk.Label(dialog, text="Move To:").pack(pady=5)
        target_var = tk.StringVar()
        targets = [l for l in self.lists if l != lst]
        target_dropdown = ttk.Combobox(
            dialog, values=targets, textvariable=target_var, state="readonly"
        )
        target_dropdown.pack(pady=5)
        target_dropdown.current(0)

        def move():
            task = task_var.get()
            target = target_var.get()
            if not task or not target:
                messagebox.showwarning("Select", "Select task and list.")
                return
            self.tasks[target][task] = self.tasks[lst].pop(task)
            self.save_data()
            self.refresh_task_display()
            dialog.destroy()

        tk.Button(dialog, text="Move", command=move).pack(pady=10)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def sort_tasks(self):
        lst = self.current_list.get()
        if lst in self.tasks:
            self.tasks[lst] = dict(sorted(self.tasks[lst].items()))
            self.save_data()
            self.refresh_task_display()

    def show_search(self):
        lst = self.current_list.get()
        if not lst or not self.tasks.get(lst):
            return messagebox.showwarning("No tasks", "No tasks in current list.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Search Tasks")
        dialog.geometry("550x400")

        tk.Label(dialog, text="Search Query:").pack(pady=5)
        query_entry = tk.Entry(dialog)
        query_entry.pack(pady=5)

        def search():
            query = query_entry.get().strip().lower()
            if not query:
                return messagebox.showwarning("Invalid query", "Enter a search query.")
            results = {}
            for task, meta in self.tasks[lst].items():
                if query in task.lower() or query in meta.get("notes", "").lower():
                    results[task] = meta
            self.show_filtered_tasks(results)
            dialog.destroy()

        tk.Button(dialog, text="Search", command=search).pack(pady=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def show_filter(self):
        lst = self.current_list.get()
        if not lst or not self.tasks.get(lst):
            return messagebox.showwarning("No tasks", "No tasks in current list.")

        dialog = tk.Toplevel(self.root)
        dialog.title("Filter Tasks")
        dialog.geometry("550x400")

        def show_filtered(completed):
            filtered = {
                k: v
                for k, v in self.tasks[lst].items()
                if v.get("completed") == completed
            }
            self.show_filtered_tasks(filtered)
            dialog.destroy()

        tk.Button(
            dialog, text="Show Completed", command=lambda: show_filtered(True)
        ).pack(pady=5)
        tk.Button(
            dialog, text="Show Incomplete", command=lambda: show_filtered(False)
        ).pack(pady=5)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)

    def show_filtered_tasks(self, tasks):
        for w in self.tasks_inner.winfo_children():
            w.destroy()
        for task, meta in tasks.items():
            var = tk.BooleanVar(value=meta.get("completed", False))
            cb = tk.Checkbutton(
                self.tasks_inner,
                text=task,
                variable=var,
                command=lambda t=task, v=var: self.toggle_completion(t, v),
            )
            cb.pack(anchor=tk.W, fill=tk.X, padx=5, pady=2)

    def export_tasks(self):
        lst = self.current_list.get()
        if not lst or lst not in self.tasks:
            return messagebox.showwarning("No list", "Select a list first.")

        file = filedialog.asksaveasfilename(
            title="Export Tasks",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
        )
        if not file:
            return

        with open(file, "w") as f:
            for t, m in self.tasks[lst].items():
                status = "Done" if m.get("completed") else "Pending"
                tags = ",".join(m.get("tags", []))
                notes = m.get("notes", "").replace("\n", " ")
                f.write(
                    f"{t} | {status} | Due: {m.get('due_date', '')} | Prog: {m.get('progress', 0)}% | Tags: {tags} | Notes: {notes}\n"
                )

        messagebox.showinfo("Export", "Tasks exported successfully.")

    def import_tasks(self):
        lst = self.current_list.get()
        if not lst:
            return messagebox.showwarning("No list", "Select a list first.")

        file = filedialog.askopenfilename(
            title="Import Tasks", filetypes=[("Text Files", "*.txt")]
        )
        if not file:
            return

        try:
            with open(file) as f:
                for line in f:
                    task = line.split("|")[0].strip()
                    if task and lst in self.tasks and task not in self.tasks[lst]:
                        self.tasks[lst][task] = {
                            "completed": False,
                            "due_date": "",
                            "reminder": "",
                            "progress": 0,
                            "notes": "",
                            "tags": [],
                            "attachment": "",
                            "priority": "Low",
                            "assignee": next(iter(self.users or {"": ""})),
                        }
            self.save_data()
            self.refresh_task_display()
            messagebox.showinfo("Import", "Tasks imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {e}")

    def check_reminders(self):
        while True:
            for lst, tasks in self.tasks.items():
                for task, meta in tasks.items():
                    reminder = meta.get("reminder")
                    if reminder:
                        now = datetime.now()
                        reminder_time = datetime.strptime(reminder, "%H:%M")
                        reminder_time = reminder_time.replace(
                            year=now.year, month=now.month, day=now.day
                        )
                        if reminder_time < now:
                            messagebox.showinfo(
                                "Reminder", f"Reminder for task '{task}'!"
                            )
            time.sleep(60)

    def center_screen(self):
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
