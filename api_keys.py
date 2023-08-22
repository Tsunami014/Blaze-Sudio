# AI generated code

import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from connect.utils.terminal.markdown import render

def how_to_get_keys():
    with open('keys/how_to_get_keys.md') as f:
        print(render(f.read()))

# Function to save API keys to a file
def save_api_keys():
    api_key = entry_api_key.get()
    api_key2 = entry_api_key2.get()
    
    # Validate input
    #if not api_key or not api_key2:
    #    messagebox.showerror("Error", "API Keys are required.")
    #    return

    # Check if the file exists and update it if necessary
    if os.path.exists('keys/apiKeys.key'):
        with open('keys/apiKeys.key', 'w') as file:
            file.write(f'API Key: {api_key}\n')
            file.write(f'Other API Key: {api_key2}\n')
        status_var.set("API keys updated successfully!")
    else:
        with open('keys/apiKeys.key', 'w') as file:
            file.write(f'API Key: {api_key}\n')
            file.write(f'Other API Key: {api_key2}\n')
        status_var.set("API keys saved successfully!")

# Function to delete API keys and show confirmation dialog
def delete_api_keys():
    result = messagebox.askquestion("Delete API Keys", "Are you sure you want to delete the API keys?")
    if result == 'yes':
        if os.path.exists('keys/apiKeys.key'):
            os.remove('keys/apiKeys.key')
            entry_api_key.delete(0, tk.END)
            entry_api_key2.delete(0, tk.END)
            status_var.set("API keys deleted successfully!")

# Function to clear the entry fields
def clear_fields():
    entry_api_key.delete(0, tk.END)
    entry_api_key2.delete(0, tk.END)

# Function to copy API keys to clipboard
def copy_to_clipboard():
    api_key = entry_api_key.get()
    api_key2 = entry_api_key2.get()
    root.clipboard_clear()
    root.clipboard_append(api_key + "\n" + api_key2)
    root.update()
    status_var.set("API keys copied to clipboard")

# Function to toggle key masking
def toggle_masking():
    if show_keys.get():
        entry_api_key.config(show="")
        entry_api_key2.config(show="")
    else:
        entry_api_key.config(show="•")
        entry_api_key2.config(show="•")

# Function to show the help page
def show_help():
    help_text = "We respect your privacy and will not abuse your data.\n\n"\
                "This application allows you to manage your API keys securely.\n"\
                "You can store, update, and delete your API keys as needed."
    messagebox.showinfo("Help", help_text)

# Create the main window
root = tk.Tk()
root.title("API Key Manager")
root.geometry("400x350")  # Set initial window size

# Set a custom font
custom_font = ("Helvetica", 12)

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Create an Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy to Clipboard", command=copy_to_clipboard)
edit_menu.add_command(label="Clear", command=clear_fields)

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_help)
help_menu.add_command(label="How to get API keys?", command=how_to_get_keys)

# Create labels and entry fields for API keys
label_api_key = tk.Label(root, text="Add your Bard API key here:", font=custom_font)
label_api_key.pack(pady=10)
entry_api_key = tk.Entry(root, show="•", font=custom_font)
entry_api_key.pack()

label_api_key2 = tk.Label(root, text="Add your Sydney API key here:", font=custom_font)
label_api_key2.pack(pady=10)
entry_api_key2 = tk.Entry(root, show="•", font=custom_font)
entry_api_key2.pack()

# Create buttons for saving, deleting, and clearing API keys
save_button = tk.Button(root, text="Save API Keys", command=save_api_keys, font=custom_font)
save_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete API Keys", command=delete_api_keys, font=custom_font)
delete_button.pack(pady=5)

copy_button = tk.Button(root, text="How do I get these API keys?", command=how_to_get_keys, font=custom_font)
copy_button.pack(pady=5)

# Create a checkbox to toggle key masking
show_keys = tk.BooleanVar()
show_keys.set(False)  # Keys are hidden by default
masking_checkbox = tk.Checkbutton(root, text="Show Keys", variable=show_keys, command=toggle_masking, font=custom_font)
masking_checkbox.pack()

# Create a status bar
status_var = tk.StringVar()
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Check if the file exists and populate the entry fields if it does
if os.path.exists('keys/apiKeys.key'):
    with open('keys/apiKeys.key', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            entry_api_key.insert(0, lines[0].split(': ')[1].strip())
            entry_api_key2.insert(0, lines[1].split(': ')[1].strip())

# Start the Tkinter main loop
root.mainloop()