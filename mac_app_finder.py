import os
import sys
import tkinter as tk
from tkinter import ttk
import subprocess
from pathlib import Path

class MacAppFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Application Finder")
        self.root.geometry("600x400")

        # Data storage
        self.apps = []  # List of dicts: {'name', 'path', 'category'}
        self.load_applications()

        # UI Layout
        self.create_widgets()
        self.update_list()

    def load_applications(self):
        """Scans common macOS application folders for .app bundles."""
        paths = [
            Path("/Applications"),
            Path("/Applications/Utilities"),
            Path("/System/Applications"),
            Path.home() / "Applications"
        ]

        seen = set()
        for base_path in paths:
            if not base_path.exists():
                continue
            for file in base_path.rglob("*.app"):
                # Avoid duplicates if same app appears in multiple locations
                real = file.resolve()
                if real in seen:
                    continue
                seen.add(real)

                name = file.stem
                # Category is the immediate parent folder name relative to base_path
                try:
                    category = file.parent.name if file.parent != base_path else "General"
                except Exception:
                    category = "General"

                self.apps.append({'name': name, 'path': str(file), 'category': category})

        # Sort alphabetically
        self.apps.sort(key=lambda x: x['name'].lower())

    def create_widgets(self):
        # Search Frame
        search_frame = ttk.Frame(self.root, padding="10")
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_list())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, expand=True)
        self.search_entry.focus_set()

        # Main Content Frame (Treeview)
        list_frame = ttk.Frame(self.root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('name', 'category')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('name', text='Application')
        self.tree.heading('category', text='Category')
        self.tree.column('category', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Close", command=self.root.destroy).pack(side=tk.RIGHT)
        ttk.Button(btn_frame, text="Launch", command=self.launch_app).pack(side=tk.RIGHT, padx=5)

        # Key Bindings
        self.root.bind('<Return>', lambda e: self.launch_app())
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.tree.bind('<Double-1>', lambda e: self.launch_app())

    def update_list(self):
        """Filters the list based on search input."""
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())

        for app in self.apps:
            if search_term in app['name'].lower() or search_term in app['category'].lower():
                # store path in tags for retrieval
                self.tree.insert('', tk.END, values=(app['name'], app['category']), tags=(app['path'],))

    def launch_app(self):
        """Opens the selected .app bundle using the macOS open command."""
        selected = self.tree.selection()
        if selected:
            app_path = self.tree.item(selected[0])['tags'][0]
            try:
                # Use 'open' so macOS handles .app bundles correctly
                subprocess.run(['open', app_path], check=False)
            except Exception as e:
                print(f"Error launching app: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MacAppFinder(root)
    root.mainloop()

