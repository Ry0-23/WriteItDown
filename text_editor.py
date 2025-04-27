import tkinter as tk
from tkinter import filedialog, messagebox, font, colorchooser
import os

def main():
    def open_file():
        filepath = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        text_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            text_edit.insert(tk.END, text)
        window.title(f"WriteItDown - {os.path.basename(filepath)}")
        global current_file
        current_file = filepath
        update_status(f"Opened: {filepath}")

    def save_file():
        global current_file
        if current_file:
            with open(current_file, "w") as output_file:
                text = text_edit.get(1.0, tk.END)
                output_file.write(text)
            update_status(f"Saved: {current_file}")
        else:
            save_as()

    def save_as():
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        with open(filepath, "w") as output_file:
            text = text_edit.get(1.0, tk.END)
            output_file.write(text)
        window.title(f"WriteItDown - {os.path.basename(filepath)}")
        global current_file
        current_file = filepath
        update_status(f"Saved as: {filepath}")

    def new_file():
        text_edit.delete(1.0, tk.END)
        window.title("WriteItDown - Untitled")
        global current_file
        current_file = None
        update_status("New file created")

    def cut_text():
        if text_edit.selection_get():
            # Save selected text to clipboard
            selected_text = text_edit.selection_get()
            window.clipboard_clear()
            window.clipboard_append(selected_text)
            # Delete selected text
            text_edit.delete(tk.SEL_FIRST, tk.SEL_LAST)
            update_status("Cut text")

    def copy_text():
        if text_edit.selection_get():
            # Save selected text to clipboard
            selected_text = text_edit.selection_get()
            window.clipboard_clear()
            window.clipboard_append(selected_text)
            update_status("Copied text")

    def paste_text():
        try:
            text_to_insert = window.clipboard_get()
            text_edit.insert(tk.INSERT, text_to_insert)
            update_status("Pasted text")
        except tk.TclError:
            update_status("Nothing to paste")

    def about():
        messagebox.showinfo(
            "About WriteItDown",
            "WriteItDown is a simple text editor created with Python and Tkinter."
        )

    def update_status(message):
        status_bar.config(text=message)
        # Clear after 3000ms
        window.after(3000, lambda: status_bar.config(text="Ready"))
    
    def update_word_count(event=None):
        text = text_edit.get(1.0, tk.END)
        words = len(text.split())
        characters = len(text) - 1  # Subtract 1 for the automatic newline
        word_count_label.config(text=f"Words: {words} | Characters: {characters}")

    def check_changes(event=None):
        update_word_count()
        # Could implement "unsaved changes" indicator here
    
    def exit_app():
        # Could implement "save before exit" dialog here
        window.destroy()
        
    def toggle_dark_mode():
        global dark_mode
        dark_mode = not dark_mode
        apply_theme()
        
    def apply_theme():
        if dark_mode:
            # Dark mode colors
            text_edit.config(bg="#282c34", fg="#abb2bf", insertbackground="#abb2bf")
            frame.config(bg="#21252b")
            status_frame.config(bg="#21252b")
            status_bar.config(bg="#21252b", fg="#abb2bf")
            word_count_label.config(bg="#21252b", fg="#abb2bf")
            
            for button in [new_button, open_button, save_button, save_as_button]:
                button.config(bg="#3e4451", fg="#abb2bf", activebackground="#4b5263", activeforeground="#ffffff")
                
            # Save theme preference
            update_status("Dark mode enabled")
        else:
            # Light mode colors
            text_edit.config(bg="white", fg="black", insertbackground="black")
            frame.config(bg=default_bg)
            status_frame.config(bg=default_bg)
            status_bar.config(bg=default_bg, fg="black")
            word_count_label.config(bg=default_bg, fg="black")
            
            for button in [new_button, open_button, save_button, save_as_button]:
                button.config(bg=default_bg, fg="black", activebackground=default_bg, activeforeground="black")
                
            # Save theme preference
            update_status("Light mode enabled")
    
    def show_font_dialog():
        root = tk.Toplevel(window)
        root.title("Font Selection")
        root.geometry("400x300")
        root.resizable(False, False)
        root.transient(window)
        root.grab_set()
        
        # Get current font from text_edit
        current_font = font.Font(font=text_edit["font"])
        current_family = current_font.actual("family")
        current_size = current_font.actual("size")
        current_weight = current_font.actual("weight")
        current_slant = current_font.actual("slant")
        
        # Create variables to store selected font properties
        family_var = tk.StringVar(value=current_family)
        size_var = tk.IntVar(value=current_size)
        bold_var = tk.BooleanVar(value=True if current_weight == "bold" else False)
        italic_var = tk.BooleanVar(value=True if current_slant == "italic" else False)
        
        # Get available font families
        font_families = sorted(list(font.families()))
        
        # Font family frame
        family_frame = tk.LabelFrame(root, text="Font Family")
        family_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        family_listbox = tk.Listbox(family_frame)
        family_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Add scrollbar to font family listbox
        family_scrollbar = tk.Scrollbar(family_frame)
        family_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        family_listbox.config(yscrollcommand=family_scrollbar.set)
        family_scrollbar.config(command=family_listbox.yview)
        
        # Add font families to listbox
        for family in font_families:
            family_listbox.insert(tk.END, family)
            
        # Select current font family
        for i, family in enumerate(font_families):
            if family == current_family:
                family_listbox.selection_set(i)
                family_listbox.see(i)
                break
        
        # Font size frame
        size_frame = tk.LabelFrame(root, text="Font Size")
        size_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Font size options
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        for size in sizes:
            rb = tk.Radiobutton(size_frame, text=str(size), variable=size_var, value=size)
            rb.pack(anchor=tk.W, side=tk.LEFT)
        
        # Font style frame
        style_frame = tk.LabelFrame(root, text="Font Style")
        style_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Bold and italic checkboxes
        bold_check = tk.Checkbutton(style_frame, text="Bold", variable=bold_var)
        bold_check.pack(side=tk.LEFT, padx=10)
        
        italic_check = tk.Checkbutton(style_frame, text="Italic", variable=italic_var)
        italic_check.pack(side=tk.LEFT, padx=10)
        
        # Preview frame
        preview_frame = tk.LabelFrame(root, text="Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        preview_text = tk.Text(preview_frame, height=3)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        preview_text.insert(tk.END, "The quick brown fox jumps over the lazy dog.")
        
        # Update preview when selection changes
        def update_preview():
            try:
                # Get selected font family
                selection = family_listbox.curselection()
                if selection:
                    selected_family = font_families[selection[0]]
                    family_var.set(selected_family)
                
                # Build font string
                font_weight = "bold" if bold_var.get() else "normal"
                font_slant = "italic" if italic_var.get() else "roman"
                font_str = (family_var.get(), size_var.get(), font_weight, font_slant)
                
                # Update preview
                preview_text.configure(font=font_str)
            except Exception as e:
                print(f"Error updating preview: {e}")
        
        # Bind events to update preview
        family_listbox.bind("<<ListboxSelect>>", lambda e: update_preview())
        size_var.trace_add("write", lambda *args: update_preview())
        bold_var.trace_add("write", lambda *args: update_preview())
        italic_var.trace_add("write", lambda *args: update_preview())
        
        # Update preview initially
        update_preview()
        
        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Apply and Cancel buttons
        cancel_button = tk.Button(button_frame, text="Cancel", command=root.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)
        
        def apply_font():
            try:
                # Get selected font family
                selection = family_listbox.curselection()
                if selection:
                    selected_family = font_families[selection[0]]
                    family_var.set(selected_family)
                
                # Build font string
                font_weight = "bold" if bold_var.get() else "normal"
                font_slant = "italic" if italic_var.get() else "roman"
                font_str = (family_var.get(), size_var.get(), font_weight, font_slant)
                
                # Apply to main text editor
                text_edit.configure(font=font_str)
                update_status(f"Font changed to {family_var.get()}, {size_var.get()}pt")
                
                # Close dialog
                root.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not apply font: {e}")
        
        apply_button = tk.Button(button_frame, text="Apply", command=apply_font)
        apply_button.pack(side=tk.RIGHT)
    
    def choose_text_color():
        color = colorchooser.askcolor(title="Select Text Color")
        if color[1]:  # If a color was chosen (not cancelled)
            text_edit.config(fg=color[1])
            update_status(f"Text color changed to {color[1]}")
    
    def choose_bg_color():
        color = colorchooser.askcolor(title="Select Background Color")
        if color[1]:  # If a color was chosen (not cancelled)
            text_edit.config(bg=color[1])
            update_status(f"Background color changed to {color[1]}")

    # Create main window
    window = tk.Tk()
    window.title("WriteItDown - Untitled")
    window.rowconfigure(0, minsize=400, weight=1)
    window.columnconfigure(1, minsize=500, weight=1)
    
    # Store default background color
    default_bg = window.cget("background")
    
    # Initialize dark mode state
    dark_mode = False
    
    # Create text widget with scrollbar
    text_edit = tk.Text(window, font="Helvetica 12")
    scrollbar = tk.Scrollbar(window, command=text_edit.yview)
    text_edit['yscrollcommand'] = scrollbar.set
    
    # Create button frame
    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    
    # Create status bar and word count
    status_frame = tk.Frame(window, relief=tk.SUNKEN, bd=1)
    status_bar = tk.Label(status_frame, text="Ready", anchor=tk.W)
    word_count_label = tk.Label(status_frame, text="Words: 0 | Characters: 0")

    # Create buttons
    new_button = tk.Button(frame, text="New", command=new_file)
    open_button = tk.Button(frame, text="Open", command=open_file)
    save_button = tk.Button(frame, text="Save", command=save_file)
    save_as_button = tk.Button(frame, text="Save As", command=save_as)
    
    # Create menu
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    
    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Save As", command=save_as)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=exit_app)
    
    # Edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=cut_text)
    edit_menu.add_command(label="Copy", command=copy_text)
    edit_menu.add_command(label="Paste", command=paste_text)
    
    # Format menu
    format_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Format", menu=format_menu)
    format_menu.add_command(label="Font...", command=show_font_dialog)
    format_menu.add_command(label="Text Color...", command=choose_text_color)
    format_menu.add_command(label="Background Color...", command=choose_bg_color)
    
    # View menu
    view_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="View", menu=view_menu)
    view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
    
    # Help menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=about)
    
    # Layout for buttons
    new_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    open_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    save_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
    save_as_button.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
    
    # Layout for main components
    frame.grid(row=0, column=0, sticky="ns")
    text_edit.grid(row=0, column=1, sticky="nsew")
    scrollbar.grid(row=0, column=2, sticky="ns")
    status_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
    status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    word_count_label.pack(side=tk.RIGHT, padx=5)
    
    # Bind events
    text_edit.bind("<KeyRelease>", check_changes)
    
    # Track the current file
    current_file = None
    
    # Start the application
    window.mainloop()

if __name__ == "__main__":
    main()