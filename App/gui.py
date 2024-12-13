import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


class FileSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Torch")
        self.geometry("600x500")

        try:
            self.iconbitmap("./Icon/icon.ico")
        except Exception as e:
            print(f"Error setting icon: {e}")

        try:
            self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file="./Icon/icon.png"))
        except Exception as e:
            print(f"Error setting title bar icon: {e}")

        self.current_directory = tk.StringVar(value=os.getcwd())
        self.copy_status = tk.StringVar(value="")

        self.notebook = ttk.Notebook(self)
        self.main_frame = tk.Frame(self.notebook)
        self.help_frame = tk.Frame(self.notebook)

        self.notebook.add(self.main_frame, text="Main")
        self.notebook.add(self.help_frame, text="Help")
        self.notebook.pack(expand=True, fill="both")

        self.create_main_tab()
        self.create_help_tab()
        self.load_directory()

    def create_main_tab(self):
        self.file_frame = tk.Frame(self.main_frame)
        self.file_frame.place(x=10, y=10, width=580, height=400)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), anchor="center")
        style.configure("Treeview", highlightthickness=0, bd=0, font=("Arial", 10))
        style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

        self.file_listbox = ttk.Treeview(
            self.file_frame, columns=("file_path",), show="headings", height=15, selectmode="extended"
        )
        self.file_listbox.heading("file_path", text="File/Folder Path")
        self.file_listbox.column("file_path", anchor="w", width=560)

        self.scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.file_listbox.pack(side="left", fill="both", expand=True)

        self.file_listbox.bind("<Double-1>", self.enter_folder)

        tk.Entry(self.main_frame, textvariable=self.current_directory, font=("Arial", 9), width=63).place(x=26, y=420)
        tk.Button(self.main_frame, relief="groove", text=":", font=("Arial", 7), command=self.select_source_directory).place(x=11, y=419)

        button_frame = tk.Frame(self.main_frame)
        button_frame.place(x=6, y=443, width=580, height=30)

        tk.Button(button_frame, text="Select All", command=self.select_all).pack(side="left", padx=5)
        tk.Button(button_frame, text="Copy Files", command=self.copy_selected_files).pack(side="left", padx=5)
        tk.Button(button_frame, text="Deselect All", command=self.deselect_all).pack(side="left", padx=5)

        tk.Label(button_frame, textvariable=self.copy_status, font=("Arial", 9), fg="blue").pack(side="left", padx=10)

        self.bind("<BackSpace>", lambda event: self.go_back())

    def create_help_tab(self):
        help_text = (
            "Help Information:\n\n"
            "- Double-click on a folder to open it and view its contents.\n"
            "- Press Backspace to go back to the parent directory.\n"
            "- Use Ctrl + Click to select multiple files or folders.\n"
            "- Use Shift + Click to select a range of files or folders.\n"
            "- Click 'Select All' to select all files and folders.\n"
            "- Click 'Deselect All' to deselect everything.\n"
            "- Click 'Copy Files' to copy the selected files and folders' content to the clipboard.\n"
            "- The clipboard content will be formatted as:\n"
            "  file_name:\n"
            "  file_content\n\n"
            "Notes:\n"
            "- Files named 'copied_text.txt' are ignored during the copy process."
        )

        help_label = tk.Label(self.help_frame, text=help_text, justify="left", font=("Arial", 10), anchor="w")
        help_label.pack(pady=10, padx=10, anchor="w")

    def select_source_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.current_directory.set(directory)
            self.load_directory()

    def load_directory(self):
        self.file_listbox.delete(*self.file_listbox.get_children())
        directory = self.current_directory.get()

        if os.path.isdir(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                self.file_listbox.insert("", "end", values=(item_path,))

    def enter_folder(self, event):
        selected_item = self.file_listbox.selection()
        if selected_item:
            folder_path = self.file_listbox.item(selected_item[0], "values")[0]
            if os.path.isdir(folder_path):
                self.current_directory.set(folder_path)
                self.load_directory()

    def go_back(self):
        current_dir = self.current_directory.get()
        parent_dir = os.path.dirname(current_dir)
        if parent_dir and os.path.isdir(parent_dir):
            self.current_directory.set(parent_dir)
            self.load_directory()

    def select_all(self):
        self.file_listbox.selection_set(self.file_listbox.get_children())

    def deselect_all(self):
        self.file_listbox.selection_remove(self.file_listbox.selection())

    def copy_selected_files(self):
        selected_items = self.file_listbox.selection()
        selected_files = [self.file_listbox.item(item, "values")[0] for item in selected_items]

        if not selected_files:
            self.copy_status.set("No files or folders selected")
            return

        try:
            output_data = ""
            for item_path in selected_files:
                output_data += self.recursively_process_path(item_path)

            self.clipboard_clear()
            self.clipboard_append(output_data)
            self.update()
            self.copy_status.set("Contents copied to clipboard!")
        except Exception as e:
            self.copy_status.set(f"Error: {str(e)}")

    def recursively_process_path(self, path):
        output_data = ""
        if os.path.isfile(path):
            if os.path.basename(path) == "copied_text.txt":
                return ""
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    file_data = file.read()
                    file_name = os.path.basename(path)
                    output_data += f"{file_name}:\n{file_data}\n\n"
            except Exception as e:
                output_data += f"Error reading {path}: {e}\n\n"
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.basename(file_path) == "copied_text.txt":
                        continue
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as file_content:
                            file_data = file_content.read()
                            file_name = os.path.basename(file_path)
                            output_data += f"{file_name}:\n{file_data}\n\n"
                    except Exception as e:
                        output_data += f"Error reading {file_path}: {e}\n\n"
        return output_data


if __name__ == "__main__":
    app = FileSelectorApp()
    app.mainloop()