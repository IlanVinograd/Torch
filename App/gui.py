import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil


class FileSelectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Torch")
        self.geometry("600x500")
        self.current_directory = tk.StringVar(value=os.getcwd())
        self.copy_status = tk.StringVar(value="")  # Status label for copy operation
        self.target_directory = None  # Store target directory for copying

        # Checkbox states
        self.checkbox_states = {}

        # Load checkbox images
        self.checkbox_checked = tk.PhotoImage(width=15, height=15, data="""
            R0lGODlhEAAQAKEDAAAAAP//AP8AACH5BAEAAAMALAAAAAAQABAAAAMrlI+py+0Po5y02ouzPgUAOw==
        """)  # Sample placeholder for checked
        self.checkbox_unchecked = tk.PhotoImage(width=15, height=15, data="""
            R0lGODlhEAAQAKEDAAAAAP8AAP8AACH5BAEAAAMALAAAAAAQABAAAAMrlI+py+0Po5y02ouzPgUAOw==
        """)

        # File List Display (Treeview)
        self.file_frame = tk.Frame(self)
        self.file_frame.place(x=10, y=10, width=580, height=400)

        # Use a tuple for columns
        self.file_listbox = ttk.Treeview(
            self.file_frame, columns=("checkbox", "file_path"), show="headings", height=15
        )
        self.file_listbox.heading("checkbox", text="")
        self.file_listbox.column("checkbox", width=30, anchor="center")
        self.file_listbox.heading("file_path", text="File Path")
        self.file_listbox.column("file_path", anchor="w", width=500)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=self.file_listbox.yview)
        self.file_listbox.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.file_listbox.pack(side="left", fill="both", expand=True)

        # Folder Browse Button and Entry (Below Treeview)
        tk.Entry(self, textvariable=self.current_directory, font=("Arial", 9), width=63).place(x=26, y=420)
        tk.Button(self, relief="groove", text=":", font=("Arial", 7), command=self.select_source_directory).place(x=11, y=419)

        # Buttons for Select/Deselect/Copy
        button_frame = tk.Frame(self)
        button_frame.place(x=10, y=450, width=580, height=30)

        tk.Button(button_frame, text="Select All", command=self.select_all_checkboxes).pack(side="left", padx=5)
        tk.Button(button_frame, text="Copy Files", command=self.copy_selected_files).pack(side="left", padx=5)
        tk.Button(button_frame, text="Deselect All", command=self.deselect_all_checkboxes).pack(side="left", padx=5)

        # Copy Status Label
        tk.Label(button_frame, textvariable=self.copy_status, font=("Arial", 9), fg="blue").pack(side="left", padx=10)

    def select_source_directory(self):
        # Open directory selection dialog for source directory
        directory = filedialog.askdirectory()
        if directory:
            self.current_directory.set(directory)
            self.load_directory()

    def load_directory(self):
        # Load files from the selected directory into the file list
        self.file_listbox.delete(*self.file_listbox.get_children())
        self.checkbox_states.clear()
        directory = self.current_directory.get()

        if os.path.isdir(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                item_id = self.file_listbox.insert(
                    "", "end", values=(self.checkbox_unchecked, item_path)
                )  # Insert a row with an unchecked checkbox
                self.checkbox_states[item_id] = False  # Initialize the checkbox state

        # Bind a click event for checkboxes
        self.file_listbox.bind("<Button-1>", self.toggle_checkbox)

    def toggle_checkbox(self, event):
        # Toggle the checkbox state on click
        region = self.file_listbox.identify("region", event.x, event.y)
        if region == "cell":  # Ensure we are clicking on a cell
            column = self.file_listbox.identify_column(event.x)
            if column == "#1":  # Checkbox column
                row_id = self.file_listbox.identify_row(event.y)
                if row_id:
                    current_state = self.checkbox_states[row_id]
                    self.checkbox_states[row_id] = not current_state  # Toggle state
                    self.file_listbox.item(
                        row_id,
                        values=(
                            self.checkbox_checked if not current_state else self.checkbox_unchecked,
                            self.file_listbox.item(row_id, "values")[1],
                        ),
                    )

    def select_all_checkboxes(self):
        # Select all checkboxes
        for item_id in self.file_listbox.get_children():
            self.checkbox_states[item_id] = True
            self.file_listbox.item(
                item_id,
                values=(
                    self.checkbox_checked,
                    self.file_listbox.item(item_id, "values")[1],
                ),
            )

    def deselect_all_checkboxes(self):
        # Deselect all checkboxes
        for item_id in self.file_listbox.get_children():
            self.checkbox_states[item_id] = False
            self.file_listbox.item(
                item_id,
                values=(
                    self.checkbox_unchecked,
                    self.file_listbox.item(item_id, "values")[1],
                ),
            )

    def copy_selected_files(self):
        # Copy selected files to the target directory
        if not self.target_directory:
            # Prompt user to select the target directory
            self.target_directory = filedialog.askdirectory()
            if not self.target_directory:
                self.copy_status.set("No target directory selected")
                return

        selected_files = [
            self.file_listbox.item(item_id, "values")[1]
            for item_id, checked in self.checkbox_states.items()
            if checked
        ]

        if not selected_files:
            self.copy_status.set("No files selected")
            return

        try:
            for file_path in selected_files:
                shutil.copy(file_path, self.target_directory)
            self.copy_status.set("Copied successfully")
        except Exception as e:
            self.copy_status.set(f"Copy failed: {str(e)}")


if __name__ == "__main__":
    app = FileSelectorApp()
    app.mainloop()