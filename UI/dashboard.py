import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import pandas as pd
import time
from PIL import Image,ImageTk
import os
import json
from core.tnx import *

script_directory = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(script_directory, "img")
data = None

# def on_enter(e):
#     e.widget['background'] = 'lightblue'

# def on_leave(e):
#     e.widget['background'] = 'SystemButtonFace'
    
    

def wallet_details():
    console_log("fetching wallet details...")
    clear_all_console()
    console_log("fetching wallet details...")
    if wallet:
        address = wallet['address']
        acct_bln = balance(address)
        console_log(f"address:{wallet['address']}")
        console_log(" ")
        console_log(f"Balance:{acct_bln}ETH")
        
        

def upload_csv():
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
              console_log(f"CSV file '{file_path}' uploaded successfully.")
              console_log(f"Max of {len(df)} entry found inside the csv file!")
              data = df.iterrows()  
            else:
              console_log(f"Empty csv file")
            # messagebox.showinfo("Upload CSV", "CSV file uploaded successfully.")
        except Exception as e:
            console_log(f"Failed to upload CSV file. Error: {e}")
            # messagebox.showerror("Upload Error", f"Failed to upload CSV file.\n{e}")
            
            

def start_transactions():
    global data

    try:
        if data:
            console_log("Starting transactions...")
            console_log(" ")
            for index, row in data:
                from_address = wallet['address']
                pk = wallet['private']
                to_address = row['address']
                amount = float(row['amount'])
                console_log(" ")
                console_log(f"Transaction processing for...\nAddress: {to_address}\nAmount: {amount}")
                tnx =  send_token(to_address, amount, from_address, pk)
                if tnx:
                  status = 'successful'
                  console_log(f"Transactions completed.for address{to_address}!. status: {status}")
                  console_log(" ")
                else:
                  status = 'failed!'
                  console_log(f"Transactions aborted! for address{to_address},check your balance and try again. status: {status}")
                  console_log(" ")
                    
                
        else:
            console_log("Csv file not uploaded!")
        
    except Exception as e:
        print(e)
        console_log(f"Failed to process transactions. Error: {e}")
        
        

def console_log(message,text=None):
    if text is None:
        console_panel.config(state=tk.NORMAL)
        console_panel.insert(tk.END, message + '\n')
        console_panel.see(tk.END)
        console_panel.config(state=tk.DISABLED)
    else:
        clear_console()
        
        
        
        
def clear_all_console():   
    console_panel.config(state=tk.NORMAL)
    console_panel.delete('1.0', tk.END)
    console_panel.config(state=tk.DISABLED)   
        
    
def clear_console():
    console_panel.config(state=tk.NORMAL)
    console_panel.delete('1.0', tk.END)
    console_panel.config(state=tk.DISABLED)
    try:
       clear_btn.destroy()
    except:
        pass
    if wallet:
      console_log(f"user address:{wallet['address']}")
      console_log(" ")
    else:
        console_log("user wallet not found!.") 
        
      
      
      
    

def account_generation():
    global clear_btn,wallet
    try:
        home_dir = os.getcwd()
        wallet_path = os.path.join(home_dir, "core/wallet.json")
        if os.path.exists(wallet_path):
            with open(wallet_path, mode='r') as file:
                wallet = json.load(file)
            if wallet:
                address = wallet['address']
                console_log(f"Address:{address}")
        else:
            console_log("New user,please wait while we are generating new wallet...")
            wallet = create_wallet()
            console_log("Wallet generating successful...")
            console_log("please write down your wallet details and keep it safe")
            console_log(" ")
            console_log(f"private key:{wallet['private']}")
            console_log(" ")
            console_log(f"address:{wallet['address']}")
            console_log(" ")
            console_log(f"mnemonic:{wallet['mnemonic']}")
            console_log(" ")
            console_log("Click the 'clear' button to clear the screen when done!")
            clear_btn = tk.Button(left_frame, text="Clear", command=clear_console)
            clear_btn.pack(pady=10,padx=2)
            
    except Exception as err:
        console_log(err)
        
        

    
def exit():
     root.destroy()
     root.quit()




def dashboard_page():
    global console_panel,root,bg_image,left_frame
    root = ThemedTk(theme="adapta")
    root.title("Crypto Wallet App")
    root.geometry("900x600") 
    bg_image = Image.open(os.path.join(path, "bg.jpg"))
    bg_image = ImageTk.PhotoImage(bg_image)
    lb1_bg = ttk.Label(root, image=bg_image)
    lb1_bg.place(x=0, y=0, relwidth=1, relheight=1)
    style = ttk.Style()
    style.configure("TFrame", background="#002B53")
    style.configure("TLabel", background="white", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    

    right_frame = ttk.Frame(root, padding="10")
    right_frame.place(relx=0.4, rely=0.05, relwidth=0.58, relheight=0.9)


    console_panel = tk.Text(right_frame, wrap='word', state=tk.DISABLED, background="black", foreground="white", font=("Helvetica", 12))
    console_panel.pack(expand=True, fill=tk.BOTH)


    left_frame = ttk.Frame(root, padding="10")
    left_frame.place(relx=0.02, rely=0.05, relwidth=0.36, relheight=0.9)
    connect_button = tk.Button(left_frame, text="Wallet details", command=wallet_details)
    connect_button.pack(pady=10, fill=tk.X)
    # connect_button.bind("<Enter>", on_enter)
    # connect_button.bind("<Leave>", on_leave)

    upload_button = tk.Button(left_frame, text="Upload CSV", command=upload_csv)
    upload_button.pack(pady=10, fill=tk.X)
    start_button = tk.Button(left_frame, text="Start Transactions", command=start_transactions)
    start_button.pack(pady=10, fill=tk.X)
    # start_button.bind("<Enter>", on_enter)
    # start_button.bind("<Leave>", on_leave)
    
    connect_button = tk.Button(left_frame, text="Exit", command=exit)
    connect_button.pack(pady=10)
    account_generation()
    root.mainloop()
    
    

    
