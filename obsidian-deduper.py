import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import threading
import string
import nltk
from nltk.corpus import stopwords
from datetime import datetime
from tkinter import font

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords', quiet=True)
STOP_WORDS = set(stopwords.words('english'))

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Obsidian Duplicate Finder")
        self.root.minsize(800, 600)

        # Apply a theme
        style = ttk.Style()
        style.theme_use('clam')

        self.vault_path = ""
        self.duplicate_groups = []
        self.file_contents = {}
        self.setup_gui()

    def setup_gui(self):
        self.create_menu()

        # Configure fonts
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=10)
        self.bold_font = self.default_font.copy()
        self.bold_font.configure(weight="bold")

        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Frame for controls
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky="ew")

        # Vault selection
        select_button = ttk.Button(
            control_frame, text="Select Vault Folder", command=self.select_folder
        )
        select_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.create_tooltip(select_button, "Select your Obsidian vault folder")

        self.folder_label = ttk.Label(
            control_frame, text="No folder selected", font=self.bold_font
        )
        self.folder_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Similarity threshold
        threshold_label = ttk.Label(
            control_frame, text="Similarity Threshold (%):"
        )
        threshold_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.threshold_var = tk.IntVar(value=80)
        threshold_spin = ttk.Spinbox(
            control_frame, from_=50, to=100, increment=5,
            textvariable=self.threshold_var, width=5
        )
        threshold_spin.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.create_tooltip(
            threshold_spin, "Set the similarity threshold for detecting duplicates"
        )

        # Find duplicates button
        find_button = ttk.Button(
            control_frame, text="Find Duplicates", command=self.find_duplicates_thread
        )
        find_button.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
        self.create_tooltip(
            find_button, "Start searching for duplicate files"
        )

        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame, orient=tk.HORIZONTAL, length=200, mode='determinate'
        )
        self.progress.grid(row=2, column=1, padx=5, pady=10, sticky=tk.W)

        # Paned window for the treeview and preview panes
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.grid(row=1, column=0, sticky="nsew")

        # Treeview frame
        tree_frame = ttk.Frame(paned_window)
        paned_window.add(tree_frame, weight=1)

        # Updated Treeview columns
        columns = ("Similarity %", "File Path", "Size", "Modified")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show='tree headings', selectmode='extended'
        )
        self.tree.heading("#0", text="Group")
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "Similarity %":
                self.tree.column(col, anchor='center', width=100)
            else:
                self.tree.column(col, anchor='w', width=150)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars for the treeview
        tree_scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=tree_scrollbar.set)
        tree_scrollbar.grid(row=0, column=1, sticky="ns")

        tree_scrollbar_horizontal = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(xscroll=tree_scrollbar_horizontal.set)
        tree_scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        # Bind selection event to update preview
        self.tree.bind('<<TreeviewSelect>>', self.update_preview)

        # Configure tree_frame
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Preview frame
        preview_frame = ttk.Frame(paned_window)
        paned_window.add(preview_frame, weight=1)

        # File preview
        file_label = ttk.Label(
            preview_frame, text="File Preview", font=self.bold_font
        )
        file_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.file_preview = tk.Text(
            preview_frame, wrap='word', font=("Consolas", 10)
        )
        self.file_preview.grid(row=1, column=0, sticky="nsew")
        file_scrollbar = ttk.Scrollbar(
            preview_frame, orient=tk.VERTICAL, command=self.file_preview.yview
        )
        self.file_preview.configure(yscroll=file_scrollbar.set)
        file_scrollbar.grid(row=1, column=1, sticky="ns")

        # Configure preview frame
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        # Delete button
        delete_button = ttk.Button(
            main_frame, text="Delete Selected Files", command=self.delete_duplicates
        )
        delete_button.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.create_tooltip(delete_button, "Delete the selected files")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w'
        )
        self.status_bar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open Vault', command=self.select_folder)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(
            label='Delete Selected Files', command=self.delete_duplicates
        )

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.show_about)

    def show_about(self):
        messagebox.showinfo(
            "About", "Obsidian Duplicate Finder\nVersion 1.1\nEnhanced GUI"
        )

    def create_tooltip(self, widget, text):
        tooltip = ToolTip(widget)
        def enter(event):
            tooltip.showtip(text)
        def leave(event):
            tooltip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.vault_path = folder_selected
            self.folder_label.config(text=self.vault_path)
            self.duplicate_groups = []
            self.clear_treeview()
            self.clear_preview()
            self.update_status("Vault folder selected.")
        else:
            self.update_status("Vault folder selection canceled.")

    def clear_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def clear_preview(self):
        self.file_preview.delete('1.0', tk.END)

    def read_markdown_files(self):
        self.file_contents = {}
        total_files = sum(len(files) for _, _, files in os.walk(self.vault_path))
        file_counter = 0
        for root_dir, dirs, files in os.walk(self.vault_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            content_processed = self.preprocess_text(content)
                            self.file_contents[file_path] = {
                                'original': content,
                                'processed': content_processed
                            }
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
                file_counter += 1
                self.update_progress(file_counter, total_files)
        self.update_status("File reading complete.")

    def preprocess_text(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = text.split()
        tokens = [word for word in tokens if word not in STOP_WORDS]
        return ' '.join(tokens)

    def update_progress(self, current, total):
        progress = int((current / total) * 100)
        self.progress['value'] = progress
        self.root.update_idletasks()

    def update_status(self, message):
        self.status_var.set(message)

    def find_duplicates_thread(self):
        threading.Thread(target=self.find_duplicates).start()

    def find_duplicates(self):
        if not self.vault_path:
            messagebox.showwarning(
                "No Folder Selected", "Please select an Obsidian vault folder first."
            )
            return

        self.progress['value'] = 0
        self.clear_treeview()
        self.clear_preview()
        self.update_status("Reading markdown files...")
        self.read_markdown_files()
        file_paths = list(self.file_contents.keys())
        contents = [
            self.file_contents[path]['processed'] for path in file_paths
        ]

        if len(contents) < 2:
            messagebox.showinfo(
                "Not Enough Files",
                "Need at least two Markdown files to find duplicates."
            )
            self.update_status("Not enough files to find duplicates.")
            return

        threshold = self.threshold_var.get() / 100.0
        self.update_status("Calculating similarities...")

        # Vectorize the contents
        vectorizer = TfidfVectorizer().fit_transform(contents)
        vectors = vectorizer.toarray()

        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(vectors)
        np.fill_diagonal(similarity_matrix, 0)

        # Group similar files and store similarities
        groups = []
        visited = set()

        for i in range(len(file_paths)):
            if i in visited:
                continue
            group_indices = {i}
            similarities = []
            stack = [i]
            while stack:
                current = stack.pop()
                for j in range(len(file_paths)):
                    if (
                        j != current and
                        j not in group_indices and
                        similarity_matrix[current][j] >= threshold
                    ):
                        group_indices.add(j)
                        stack.append(j)
                        similarities.append(similarity_matrix[current][j])
            if len(group_indices) > 1:
                group_similarities = {
                    'indices': group_indices,
                    'similarities': similarities
                }
                groups.append(group_similarities)
                visited.update(group_indices)

        self.duplicate_groups = []
        total_groups = len(groups)
        group_counter = 0

        for group in groups:
            indices = group['indices']
            similarities = group['similarities']
            file_group = [file_paths[index] for index in indices]
            if similarities:
                avg_similarity = np.mean(similarities) * 100  # Convert to percentage
            else:
                avg_similarity = threshold * 100  # If only two files, use threshold
            self.duplicate_groups.append({
                'files': file_group,
                'similarity': round(avg_similarity, 2)
            })
            group_counter += 1
            progress = int((group_counter / total_groups) * 100)
            self.progress['value'] = progress
            self.root.update_idletasks()

        self.populate_treeview()
        self.update_status("Duplicate search complete.")
        messagebox.showinfo(
            "Duplicates Found", f"Found {len(self.duplicate_groups)} duplicate groups."
        )

    def get_file_info(self, file_path):
        stats = os.stat(file_path)
        size = self.human_readable_size(stats.st_size)
        mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        return {'size': size, 'mtime': mtime}

    @staticmethod
    def human_readable_size(size, decimal_places=2):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.{decimal_places}f} {unit}"
            size /= 1024.0
        return f"{size:.{decimal_places}f} TB"

    def populate_treeview(self):
        self.clear_treeview()
        for idx, group in enumerate(self.duplicate_groups):
            group_id = f"group_{idx}"
            similarity = group['similarity']
            self.tree.insert(
                '', tk.END, iid=group_id,
                text=f"Group {idx+1} ({len(group['files'])} files)",
                values=(f"{similarity}%", "", "", "")
            )
            for file_path in group['files']:
                file_rel = os.path.relpath(file_path, self.vault_path)
                file_info = self.get_file_info(file_path)
                self.tree.insert(
                    group_id, tk.END, values=(
                        "",  # Empty similarity for files
                        file_rel,
                        file_info['size'],
                        file_info['mtime']
                    )
                )

    def update_preview(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        # For simplicity, only show the first selected file
        item = selected_items[0]
        parent = self.tree.parent(item)
        if parent:
            # It's a file item
            file_rel = self.tree.item(item, 'values')[1]
            file_path = os.path.join(self.vault_path, file_rel)

            self.file_preview.delete('1.0', tk.END)
            try:
                content = self.file_contents[file_path]['original']
                self.file_preview.insert(tk.END, content)
            except KeyError:
                self.file_preview.insert(tk.END, "Unable to load content.")
        else:
            # It's a group item
            self.file_preview.delete('1.0', tk.END)

    def delete_duplicates(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning(
                "No Selection", "Please select files or groups to delete."
            )
            return

        deleted_files = []

        for item in selected_items:
            parent = self.tree.parent(item)
            if parent:
                # It's a file item
                file_rel = self.tree.item(item, 'values')[1]
                file_path = os.path.join(self.vault_path, file_rel)
                files_to_delete = [file_path]
                group_id = parent
            else:
                # It's a group item
                group_id = item
                # Get all file paths in the group
                files_in_group = []
                for child in self.tree.get_children(item):
                    file_rel = self.tree.item(child, 'values')[1]
                    file_path = os.path.join(self.vault_path, file_rel)
                    files_in_group.append(file_path)

                # Use the custom dialog to select files to delete
                files_to_delete = self.ask_files_to_delete(files_in_group)
                if not files_to_delete:
                    continue  # Skip deletion for this group

            for file_to_delete in files_to_delete:
                try:
                    os.remove(file_to_delete)
                    deleted_files.append(file_to_delete)
                    # Remove from Treeview and internal data
                    items_to_remove = []
                    for child in self.tree.get_children(group_id):
                        file_rel = self.tree.item(child, 'values')[1]
                        file_path = os.path.join(self.vault_path, file_rel)
                        if file_path == file_to_delete:
                            items_to_remove.append(child)
                            break  # Each file appears only once
                    for i in items_to_remove:
                        self.tree.delete(i)
                    if file_to_delete in self.file_contents:
                        del self.file_contents[file_to_delete]
                except Exception as e:
                    messagebox.showerror(
                        "Error Deleting File", f"Could not delete {file_to_delete}: {e}"
                    )

            # If all files in the group are deleted, remove the group
            if not self.tree.get_children(group_id):
                self.tree.delete(group_id)

        if deleted_files:
            messagebox.showinfo(
                "Deletion Complete", f"Deleted {len(deleted_files)} files."
            )
            self.update_status(f"Deleted {len(deleted_files)} files.")

    def ask_files_to_delete(self, file_paths):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Files to Delete")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("400x300")

        label = ttk.Label(
            dialog, text="Select the files you want to delete:", font=self.bold_font
        )
        label.pack(pady=10)

        files_var = {}
        for file_path in file_paths:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(
                dialog,
                text=os.path.relpath(file_path, self.vault_path),
                variable=var
            )
            chk.pack(anchor='w', padx=20)
            files_var[file_path] = var

        def on_confirm():
            selected_files = [
                fp for fp, var in files_var.items() if var.get()
            ]
            if not selected_files:
                messagebox.showwarning(
                    "No Files Selected",
                    "You must select at least one file to delete."
                )
                return
            self._files_to_delete = selected_files
            dialog.destroy()

        confirm_button = ttk.Button(
            dialog, text="Delete Selected Files", command=on_confirm
        )
        confirm_button.pack(pady=10)

        dialog.wait_window()
        return getattr(self, '_files_to_delete', [])

class ToolTip:
    """
    Class to create a tooltip for a given widget
    """
    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def showtip(self, text):
        "Display text in tooltip window"
        if self.tip_window or not text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=text, background="lightyellow", relief='solid',
            borderwidth=1, font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()
