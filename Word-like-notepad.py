import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
from tkinter.colorchooser import askcolor
import os
import json
from datetime import datetime
from PIL import Image, ImageTk


class WordLikeNotepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Word-like Notepad")
        self.master.geometry("800x600")  # Set initial size
        self.master.minsize(400, 300)  # Set minimum size

        self.filename = None
        self.settings = self.load_settings()
        self.default_font = font.Font(family="Arial", size=12)

        """ self.download_icons()  # Download icons before creating UI elements """

        self.create_text_widget()
        self.create_menu()
        self.create_toolbar()
        self.create_format_bar()
        self.create_status_bar()

        self.apply_theme(self.settings.get("theme", "light"))

        self.content_saved = True
        self.text_widget.bind("<<Modified>>", self.on_content_modified)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def download_icons(self):
        icons = {
            "new": "https://raw.githubusercontent.com/google/material-design-icons/master/png/file/create_new_folder/materialicons/24dp/2x/baseline_create_new_folder_black_24dp.png",
            "open": "https://raw.githubusercontent.com/google/material-design-icons/master/png/file/folder_open/materialicons/24dp/2x/baseline_folder_open_black_24dp.png",
            "save": "https://raw.githubusercontent.com/google/material-design-icons/master/png/content/save/materialicons/24dp/2x/baseline_save_black_24dp.png",
            "bold": "https://raw.githubusercontent.com/google/material-design-icons/master/png/editor/format_bold/materialicons/24dp/2x/baseline_format_bold_black_24dp.png",
            "italic": "https://raw.githubusercontent.com/google/material-design-icons/master/png/editor/format_italic/materialicons/24dp/2x/baseline_format_italic_black_24dp.png",
            "underline": "https://raw.githubusercontent.com/google/material-design-icons/master/png/editor/format_underlined/materialicons/24dp/2x/baseline_format_underlined_black_24dp.png",
        }

        if not os.path.exists("icons"):
            os.makedirs("icons")

        """ for name, url in icons.items():
            if not os.path.exists(f"icons/{name}.png"):
                response = requests.get(url)
                img = Image.open(io.BytesIO(response.content))
                img.save(f"icons/{name}.png")
        """

    def load_settings(self):
        settings_file = "notepad_settings.json"
        default_settings = {
            "font_family": "Arial",
            "font_size": 12,
            "theme": "light",
        }

        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Error reading settings file. Using default settings.")
                    return default_settings
        else:
            print("Settings file not found. Using default settings.")
            return default_settings

    def save_settings(self):
        settings_file = "word_like_notepad_settings.json"
        with open(settings_file, "w") as f:
            json.dump(self.settings, f)

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.LEFT, fill=tk.X)

        self.new_icon = ImageTk.PhotoImage(Image.open("icons/new.png"))
        self.open_icon = ImageTk.PhotoImage(Image.open("icons/open.png"))
        self.save_icon = ImageTk.PhotoImage(Image.open("icons/save.png"))

        self.bold_icon = ImageTk.PhotoImage(Image.open("icons/bold.png"))
        self.italic_icon = ImageTk.PhotoImage(Image.open("icons/italic.png"))
        self.underline_icon = ImageTk.PhotoImage(Image.open("icons/underline.png"))

        ttk.Button(self.toolbar, image=self.new_icon, command=self.new_file).pack(
            side=tk.LEFT,
            padx=2,
            pady=2,
        )
        ttk.Button(self.toolbar, image=self.open_icon, command=self.open_file).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        ttk.Button(self.toolbar, image=self.save_icon, command=self.save_file).pack(
            side=tk.LEFT, padx=2, pady=2
        )

        ttk.Button(self.toolbar, image=self.bold_icon, command=self.toggle_bold).pack(
            side=tk.LEFT, padx=2, pady=2
        )
        ttk.Button(
            self.toolbar, image=self.italic_icon, command=self.toggle_italic
        ).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(
            self.toolbar, image=self.underline_icon, command=self.toggle_underline
        ).pack(side=tk.LEFT, padx=2, pady=2)

    def create_text_widget(self):
        self.text_frame = ttk.Frame(self.master)
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        # Text Widget
        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, undo=True)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.text_widget, orient=tk.VERTICAL, command=self.text_widget.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure scrollbar and line numbers
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Bind events
        self.text_widget.bind("<KeyPress>", self.on_key_press)
        self.text_widget.bind("<KeyRelease>", self.on_key_press)
        self.text_widget.config(
            yscrollcommand=lambda *args: (self.scrollbar.set(*args))
        )

        # Ensure line numbers width stays fixed
        self.text_widget.grid_columnconfigure(0, minsize=1)  # Adjust as needed

    def create_format_bar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.fonts = font.families()
        self.font_family = tk.StringVar()
        self.font_family.set("Arial")
        self.font_size = tk.StringVar()
        self.font_size.set("12")

        font_dropdown = ttk.Combobox(
            self.toolbar,
            textvariable=self.font_family,
            values=self.fonts,
            state="readonly",
        )
        font_dropdown.pack(side=tk.LEFT, padx=2, pady=2)
        font_dropdown.bind("<<ComboboxSelected>>", self.change_font)

        size_dropdown = ttk.Combobox(
            self.toolbar,
            textvariable=self.font_size,
            values=list(range(8, 73)),
            state="readonly",
        )
        size_dropdown.pack(side=tk.LEFT, padx=2, pady=2)
        size_dropdown.bind("<<ComboboxSelected>>", self.change_font)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(
            label="Undo", command=lambda: self.text_widget.edit_undo()
        )
        edit_menu.add_command(
            label="Redo", command=lambda: self.text_widget.edit_redo()
        )
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

        # Insert menu
        insert_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Insert", menu=insert_menu)
        insert_menu.add_command(label="Image", command=self.insert_image)
        insert_menu.add_command(label="Table", command=self.insert_table)

        # Format menu
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font", command=self.change_font)
        format_menu.add_command(label="Text Color", command=self.change_text_color)
        format_menu.add_command(label="Background Color", command=self.change_bg_color)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Word Count", command=self.word_count)
        tools_menu.add_command(label="Find and Replace", command=self.find_replace)
        tools_menu.add_command(label="Spell Check", command=self.spell_check)

    def insert_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300))  # Resize image
            photo = ImageTk.PhotoImage(image)
            self.text_widget.image_create(tk.END, image=photo)
            self.image = photo  # Keep a reference

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.master, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Ensure the status bar expands correctly
        self.status_bar.grid_columnconfigure(0, weight=1)
        self.status_bar.grid_rowconfigure(1, weight=0)

    def new_file(self):
        self.filename = None
        self.text_widget.delete(1.0, tk.END)
        self.update_status("New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, content)
                self.filename = file_path
                self.update_status(f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open file: {str(e)}")

    def save_file(self):
        if self.filename:
            file_path = self.filename  # Use existing filename if set
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            )
            if not file_path:
                return  # User cancelled save operation

            self.filename = file_path  # Set filename for subsequent saves
            self.master.title(f"Word-like Notepad - {os.path.basename(file_path)}")

        with open(self.filename, "w") as file:
            file.write(self.text_widget.get(1.0, tk.END))

        self.content_saved = True
        self.status_bar.config(text="Saved")

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            self.filename = file_path
            self.save_file()

    def on_content_modified(self, event=None):
        self.content_saved = False
        self.text_widget.edit_modified(0)

    def on_close(self):
        if not self.content_saved:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before exiting?",
            )
            if response:  # Save and exit
                self.save_file()
                self.master.destroy()
            elif response is False:  # Discard and exit
                self.master.destroy()
            # If response is None (Cancel), do nothing
        else:
            self.master.destroy()

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def toggle_dark_mode(self):
        if self.settings.get("theme", "light") == "light":
            self.apply_theme("dark")
        else:
            self.apply_theme("light")

    def apply_theme(self, theme):
        if theme == "dark":
            self.text_widget.config(
                bg="#1e1e1e", fg="#ffffff", insertbackground="white"
            )
        else:
            self.text_widget.config(
                bg="#ffffff", fg="#000000", insertbackground="black"
            )
        self.settings["theme"] = theme
        self.save_settings()

    def word_count(self):
        content = self.text_widget.get(1.0, tk.END)
        words = len(content.split())
        chars = len(content)
        lines = int(self.text_widget.index("end-1c").split(".")[0])
        messagebox.showinfo(
            "Word Count", f"Words: {words}\nCharacters: {chars}\nLines: {lines}"
        )

    def find_replace(self):
        top = tk.Toplevel(self.master)
        top.title("Find and Replace")
        top.geometry("300x150")

        ttk.Label(top, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = ttk.Entry(top, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = ttk.Entry(top, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            top, text="Find", command=lambda: self.find_text(find_entry.get())
        ).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(
            top,
            text="Replace",
            command=lambda: self.replace_text(find_entry.get(), replace_entry.get()),
        ).grid(row=2, column=1, padx=5, pady=5)

    def find_text(self, query):
        self.text_widget.tag_remove("found", "1.0", tk.END)
        if query:
            idx = "1.0"
            while True:
                idx = self.text_widget.search(query, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = f"{idx}+{len(query)}c"
                self.text_widget.tag_add("found", idx, lastidx)
                idx = lastidx
            self.text_widget.tag_config("found", foreground="red", background="yellow")

    def replace_text(self, find_query, replace_query):
        self.text_widget.tag_remove("found", "1.0", tk.END)
        if find_query and replace_query:
            idx = "1.0"
            while True:
                idx = self.text_widget.search(
                    find_query, idx, nocase=1, stopindex=tk.END
                )
                if not idx:
                    break
                lastidx = f"{idx}+{len(find_query)}c"
                self.text_widget.delete(idx, lastidx)
                self.text_widget.insert(idx, replace_query)
                lastidx = f"{idx}+{len(replace_query)}c"
                self.text_widget.tag_add("found", idx, lastidx)
                idx = lastidx
            self.text_widget.tag_config(
                "found", foreground="green", background="yellow"
            )

    def on_key_press(self, event=None):
        self.update_status("Editing")

    def update_status(self, message):
        self.status_bar.config(
            text=f"{message} | {datetime.now().strftime('%H:%M:%S')}"
        )

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def change_font(self, event=None):
        font_family = self.font_family.get()
        font_size = int(self.font_size.get())

        # Determine current tags on selected text
        if self.text_widget.tag_ranges("sel"):
            start, end = self.text_widget.tag_ranges("sel")
            current_tags = self.text_widget.tag_names(start)
        else:
            return  # No selected text, do nothing

        # Update font style based on dropdown selections
        font_style = ""
        if "bold" in current_tags:
            font_style += " bold"
        if "italic" in current_tags:
            font_style += " italic"
        if "underline" in current_tags:
            font_style += " underline"

        # Create or update font tag for selected text
        font_tag = f"{font_family}_{font_size}_{font_style}"
        self.text_widget.tag_configure(
            font_tag, font=(font_family, font_size, font_style.strip())
        )

        # Apply tag to selected text
        self.text_widget.tag_add(font_tag, start, end)

        # Remove previous font tags from selected text
        for tag in current_tags:
            if (
                tag.startswith(("Arial_", "12_", "bold", "italic", "underline"))
                and tag != font_tag
            ):
                self.text_widget.tag_remove(tag, start, end)

        # Save font settings (optional)
        self.settings["font_family"] = font_family
        self.settings["font_size"] = font_size
        self.save_settings()

    def toggle_theme(self):
        if self.settings["theme"] == "light":
            self.settings["theme"] = "dark"
        else:
            self.settings["theme"] = "light"
        self.apply_theme(self.settings["theme"])
        self.save_settings()

    def change_text_color(self):
        color = askcolor(title="Choose text color")[1]
        if color:
            current_tags = self.text_widget.tag_names("sel.first")
            self.text_widget.tag_configure(f"color_{color}", foreground=color)
            if "sel" in self.text_widget.tag_names():
                self.text_widget.tag_add(f"color_{color}", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add(f"color_{color}", "insert")
            for tag in current_tags:
                if tag.startswith("color_"):
                    self.text_widget.tag_remove(tag, "sel.first", "sel.last")

    def change_bg_color(self):
        color = askcolor(title="Choose background color")[1]
        if color:
            current_tags = self.text_widget.tag_names("sel.first")
            self.text_widget.tag_configure(f"bg_{color}", background=color)
            if "sel" in self.text_widget.tag_names():
                self.text_widget.tag_add(f"bg_{color}", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add(f"bg_{color}", "insert")
            for tag in current_tags:
                if tag.startswith("bg_"):
                    self.text_widget.tag_remove(tag, "sel.first", "sel.last")

    def toggle_bold(self):
        if self.text_widget.tag_ranges("sel"):
            current_tags = self.text_widget.tag_names("sel.first")
            if "bold" in current_tags:
                self.text_widget.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("bold", "sel.first", "sel.last")

            # Update font with current settings
            self.change_font()

    def toggle_italic(self):
        if self.text_widget.tag_ranges("sel"):
            current_tags = self.text_widget.tag_names("sel.first")
            if "italic" in current_tags:
                self.text_widget.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("italic", "sel.first", "sel.last")

            # Update font with current settings
            self.change_font()

    def toggle_underline(self):
        if self.text_widget.tag_ranges("sel"):
            current_tags = self.text_widget.tag_names("sel.first")
            if "underline" in current_tags:
                self.text_widget.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text_widget.tag_add("underline", "sel.first", "sel.last")

            # Update font with current settings
            self.change_font()

    def insert_table(self):
        top = tk.Toplevel(self.master)
        top.title("Insert Table")
        top.geometry("250x150")

        ttk.Label(top, text="Rows:").grid(row=0, column=0, padx=5, pady=5)
        rows_entry = ttk.Entry(top, width=10)
        rows_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(top, text="Columns:").grid(row=1, column=0, padx=5, pady=5)
        cols_entry = ttk.Entry(top, width=10)
        cols_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            top,
            text="Insert",
            command=lambda: self.create_table(
                int(rows_entry.get()), int(cols_entry.get())
            ),
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def create_table(self, rows, cols):
        table = "|"
        for _ in range(cols):
            table += " Column |"
        table += "\n|"
        for _ in range(cols):
            table += "---------|"
        table += "\n"
        for _ in range(rows):
            table += "|"
            for _ in range(cols):
                table += "         |"
            table += "\n"
        self.text_widget.insert(tk.END, table)

    def spell_check(self):
        # This is a simplified spell check. For a real application, you'd want to use a proper spell checking library.
        words = self.text_widget.get("1.0", tk.END).split()
        misspelled = []
        for word in words:
            if not self.is_word(word):
                misspelled.append(word)
        if misspelled:
            messagebox.showinfo(
                "Spell Check", f"Potentially misspelled words: {', '.join(misspelled)}"
            )
        else:
            messagebox.showinfo("Spell Check", "No spelling errors found.")

    def is_word(self, word):
        # This is a very basic check. In a real application, you'd use a dictionary or language model.
        return word.isalpha()


if __name__ == "__main__":
    root = tk.Tk()
    app = WordLikeNotepad(root)
    root.mainloop()
