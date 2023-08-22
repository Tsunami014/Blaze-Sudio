# AI generated code

import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# Function to save API keys to a file
def save_api_keys():
    api_key = entry_api_key.get()
    secret_key = entry_secret_key.get()
    
    # Validate input
    if not api_key or not secret_key:
        messagebox.showerror("Error", "API Key and Secret Key are required.")
        return

    # Check if the file exists and update it if necessary
    if os.path.exists('api_keys.txt'):
        with open('api_keys.txt', 'w') as file:
            file.write(f'API Key: {api_key}\n')
            file.write(f'Secret Key: {secret_key}\n')
        status_var.set("API keys updated successfully!")
    else:
        with open('api_keys.txt', 'w') as file:
            file.write(f'API Key: {api_key}\n')
            file.write(f'Secret Key: {secret_key}\n')
        status_var.set("API keys saved successfully!")

# Function to delete API keys and show confirmation dialog
def delete_api_keys():
    result = messagebox.askquestion("Delete API Keys", "Are you sure you want to delete the API keys?")
    if result == 'yes':
        if os.path.exists('api_keys.txt'):
            os.remove('api_keys.txt')
            entry_api_key.delete(0, tk.END)
            entry_secret_key.delete(0, tk.END)
            status_var.set("API keys deleted successfully!")

# Function to clear the entry fields
def clear_fields():
    entry_api_key.delete(0, tk.END)
    entry_secret_key.delete(0, tk.END)

# Function to copy API keys to clipboard
def copy_to_clipboard():
    api_key = entry_api_key.get()
    secret_key = entry_secret_key.get()
    root.clipboard_clear()
    root.clipboard_append(api_key + "\n" + secret_key)
    root.update()
    status_var.set("API keys copied to clipboard")

# Function to toggle key masking
def toggle_masking():
    if show_keys.get():
        entry_api_key.config(show="")
        entry_secret_key.config(show="")
    else:
        entry_api_key.config(show="•")
        entry_secret_key.config(show="•")

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

# Create a Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_help)

# Create labels and entry fields for API keys
label_api_key = tk.Label(root, text="Add your API key here:", font=custom_font)
label_api_key.pack(pady=10)
entry_api_key = tk.Entry(root, show="•", font=custom_font)
entry_api_key.pack()

label_secret_key = tk.Label(root, text="Add your Secret key here:", font=custom_font)
label_secret_key.pack(pady=10)
entry_secret_key = tk.Entry(root, show="•", font=custom_font)
entry_secret_key.pack()

# Create buttons for saving, deleting, and clearing API keys
save_button = tk.Button(root, text="Save API Keys", command=save_api_keys, font=custom_font)
save_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete API Keys", command=delete_api_keys, font=custom_font)
delete_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear", command=clear_fields, font=custom_font)
clear_button.pack(pady=5)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=custom_font)
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
if os.path.exists('api_keys.txt'):
    with open('api_keys.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            entry_api_key.insert(0, lines[0].split(': ')[1].strip())
            entry_secret_key.insert(0, lines[1].split(': ')[1].strip())

# Start the Tkinter main loop
root.mainloop()