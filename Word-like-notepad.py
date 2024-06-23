import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
from tkinter.colorchooser import askcolor
import os
import json
from datetime import datetime
from PIL import Image, ImageTk
import requests
import io


class WordLikeNotepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Word-like Notepad")
        self.master.geometry("1000x700")

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

    def create_toolbar(self):
        self.toolbar = ttk.Frame(self.master)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.new_icon = ImageTk.PhotoImage(Image.open("icons/new.png"))
        self.open_icon = ImageTk.PhotoImage(Image.open("icons/open.png"))
        self.save_icon = ImageTk.PhotoImage(Image.open("icons/save.png"))

        self.bold_icon = ImageTk.PhotoImage(Image.open("icons/bold.png"))
        self.italic_icon = ImageTk.PhotoImage(Image.open("icons/italic.png"))
        self.underline_icon = ImageTk.PhotoImage(Image.open("icons/underline.png"))

        ttk.Button(self.toolbar, image=self.new_icon, command=self.new_file).pack(
            side=tk.LEFT, padx=2, pady=2
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

    def create_format_bar(self):
        self.format_bar = ttk.Frame(self.master)
        self.format_bar.pack(side=tk.TOP, fill=tk.X)

        self.fonts = font.families()
        self.font_family = tk.StringVar()
        self.font_family.set("Arial")
        self.font_size = tk.StringVar()
        self.font_size.set("12")

        font_dropdown = ttk.Combobox(
            self.format_bar, textvariable=self.font_family, values=self.fonts
        )
        font_dropdown.pack(side=tk.LEFT, padx=2, pady=2)
        font_dropdown.bind("<<ComboboxSelected>>", self.change_font)

        size_dropdown = ttk.Combobox(
            self.format_bar, textvariable=self.font_size, values=list(range(8, 73))
        )
        size_dropdown.pack(side=tk.LEFT, padx=2, pady=2)
        size_dropdown.bind("<<ComboboxSelected>>", self.change_font)

    def create_text_widget(self):
        self.text_frame = ttk.Frame(self.master)
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        self.text_widget = tk.Text(self.text_frame, wrap=tk.WORD, undo=True)
        self.text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.scrollbar = ttk.Scrollbar(
            self.text_frame, orient=tk.VERTICAL, command=self.text_widget.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.line_numbers = tk.Text(
            self.text_frame,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background="lightgrey",
            state="disabled",
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_widget.bind("<Key>", self.on_key_press)
        self.text_widget.bind("<MouseWheel>", self.on_mousewheel)

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
        view_menu.add_command(
            label="Toggle Line Numbers", command=self.toggle_line_numbers
        )
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

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.master, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
            try:
                content = self.text_widget.get(1.0, tk.END)
                with open(self.filename, "w") as file:
                    file.write(content)
                self.update_status(f"Saved: {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to save file: {str(e)}")
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            self.filename = file_path
            self.save_file()

    def cut(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste(self):
        self.text_widget.event_generate("<<Paste>>")

    def toggle_line_numbers(self):
        if self.line_numbers.winfo_viewable():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

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
            self.line_numbers.config(bg="#2d2d2d", fg="#ffffff")
        else:
            self.text_widget.config(
                bg="#ffffff", fg="#000000", insertbackground="black"
            )
            self.line_numbers.config(bg="lightgrey", fg="#000000")
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
        self.update_line_numbers()
        self.update_status("Editing")

    def on_mousewheel(self, event=None):
        self.update_line_numbers()

    def update_line_numbers(self):
        if not self.line_numbers.winfo_viewable():
            return
        self.line_numbers.config(state="normal")
        self.line_numbers.delete(1.0, tk.END)
        number_of_lines = self.text_widget.index("end-1c").split(".")[0]
        line_numbers_string = "\n".join(
            str(no + 1) for no in range(int(number_of_lines))
        )
        self.line_numbers.insert(1.0, line_numbers_string)
        self.line_numbers.config(state="disabled")

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

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def change_font(self, event=None):
        try:
            font_family = self.font_family.get()
            font_size = int(self.font_size.get())
            current_tags = self.text_widget.tag_names("sel.first")

            if "bold" in current_tags:
                font_weight = "bold"
            else:
                font_weight = "normal"

            if "italic" in current_tags:
                font_slant = "italic"
            else:
                font_slant = "roman"

            if "underline" in current_tags:
                font_underline = 1
            else:
                font_underline = 0

            new_font = font.Font(
                family=font_family,
                size=font_size,
                weight=font_weight,
                slant=font_slant,
                underline=font_underline,
            )

            # Apply the new font to the selected text or all text if no selection
            if self.text_widget.tag_ranges("sel"):
                self.text_widget.tag_configure("custom_font", font=new_font)
                self.text_widget.tag_add("custom_font", "sel.first", "sel.last")
            else:
                self.text_widget.configure(font=new_font)

            # Update the default font for future text input
            self.default_font.configure(family=font_family, size=font_size)

        except tk.TclError:
            # Handle the case where an invalid font or size is selected
            pass

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
        current_tags = self.text_widget.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_widget.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("bold", "sel.first", "sel.last")
        self.text_widget.tag_configure(
            "bold", font=(self.font_family.get(), int(self.font_size.get()), "bold")
        )
        self.change_font()

    def toggle_italic(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_widget.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("italic", "sel.first", "sel.last")
        self.text_widget.tag_configure(
            "italic", font=(self.font_family.get(), int(self.font_size.get()), "italic")
        )
        self.change_font()

    def toggle_underline(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_widget.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_widget.tag_add("underline", "sel.first", "sel.last")
        self.text_widget.tag_configure("underline", underline=True)
        self.change_font()

    def insert_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300))  # Resize image
            photo = ImageTk.PhotoImage(image)
            self.text_widget.image_create(tk.END, image=photo)
            self.text_widget.image = photo  # Keep a reference

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
