import tkinter as tk
from tkinter import ttk

# Create the main application window
root = tk.Tk()
root.title("Console Input Example")
root.geometry("600x400")

# Create the Text widget for logs
console_panel = tk.Text(root, wrap='word', state=tk.DISABLED, background="black", foreground="white", font=("Helvetica", 12))
console_panel.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

# Create the Entry widget for user input
input_frame = ttk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=5)

user_input = ttk.Entry(input_frame, font=("Helvetica", 12))
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

send_button = ttk.Button(input_frame, text="Send", command=lambda: capture_input(user_input.get()))
send_button.pack(side=tk.RIGHT, padx=5, pady=5)

def console_log(message):
    console_panel.config(state=tk.NORMAL)
    console_panel.insert(tk.END, message + '\n')
    console_panel.see(tk.END)
    console_panel.config(state=tk.DISABLED)

def capture_input(input_text):
    if input_text.strip():
        console_log(f"User: {input_text}")
        # user_input.delete(0, tk.END)

# Bind the Return key to the Entry widget
user_input.bind("<Return>", lambda event: capture_input(user_input.get()))

# Start the main event loop
root.mainloop()
