import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import pandas as pd
import time
from PIL import Image,ImageTk
import os
import json
import sys
from web3 import Web3
from eth_account import Account
import json
import asyncio
from mnemonic import Mnemonic
import os
import sys






url = "https://sepolia.base.org"

erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]


w3 = Web3(Web3.HTTPProvider(url))




def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both dev and PyInstaller bundle """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def balance(address):
    get_balance = w3.eth.get_balance(w3.to_checksum_address(address))
    balance = w3.from_wei(get_balance, "ether")
    return format(float(balance),'.3f')


def create_wallet():
    account = w3.eth.account.create()
    private_key = account._private_key.hex()
    address = account.address
    data = {
        "private": private_key,
        "address": address
    }
    wallet_path = resource_path("core/wallet.json")
    os.makedirs(os.path.dirname(wallet_path), exist_ok=True)
    with open(wallet_path, mode='w') as file:
        json.dump(data,file)
    return data


def get_wallet():
    try:
        wallet_path = resource_path("core/wallet.json")
        with open(wallet_path) as wb:
            data = json.load(wb)
        
        wallet = w3.eth.account.from_key(data['private_key'])
        return wallet
    
    except Exception as e:
        return None

def link_wallet(private_key):
    try:
        account = w3.eth.account.from_key(private_key)
        address = w3.to_checksum_address(account.address)
        print("Public Address:", account.address)
        data = {
            "private": private_key,
            "address": address,
            "mnemonic": "is a link account, no mnemonic words",
        }
        return True
    except Exception as arr:
        print(arr)
        return False


# bulding the transaction
def build_tnx(To: str, value: float, From: str, w3=w3):
    transaction = {
        "from": From,  # w3.to_checksum_address(From),
        "to": w3.to_checksum_address(To),
        "value": w3.to_wei(value, "ether"),
        "nonce": w3.eth.get_transaction_count(From),
        "gas": 21000,
        "maxFeePerGas": w3.to_wei(20, "gwei"),
        "maxPriorityFeePerGas": w3.to_wei(10, "gwei"),
        "chainId": int(w3.net.version),
    }
    return transaction


# signing the transaction
def sign_tnx(trnx, private_key: str):
    sign_tx = w3.eth.account.sign_transaction(trnx, private_key)
    return sign_tx


# sending a transaction
def send_tnx(to_address: str,from_address,pk, value=0.0001):  #
    try:

        # with open(username+".json","r") as file:
        #    data = json.load(file)
        address = w3.to_checksum_address(from_address)
        transaction = build_tnx(to_address, value, address)
        sign_tx = sign_tnx(transaction, pk)
        tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
        tx = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"transaction receit {tx}")
        if tx is None:
            return None
        else:
            if tx.status == 1:

                return tx_hash.hex()
            else:
                return None
    except Exception as arr:
        print(arr)
        return None
    
    
    


def send_token(to_ : str, amount : float | int, from_address : str, private_key : str,contract_address:str):
    token_address = w3.to_checksum_address(contract_address)
    token_contract = w3.eth.contract(address=token_address, abi = erc20_abi)
    decimals = token_contract.functions.decimals().call()
    amount_ = int(amount  * 10**decimals)
    address = w3.to_checksum_address(from_address)
    account = w3.eth.account.from_key(private_key)
    tx_params = token_contract.functions.transfer(to_, amount_).build_transaction(
        {
            "from": address,
            "nonce": w3.eth.get_transaction_count(address),
            "gasPrice": w3.eth.gas_price,
            "value": 0,
        }
    )
    
    gas = w3.eth.estimate_gas(tx_params)
    print(f"Gas is {gas}")
    tx_params["gas"] = gas
    signed_tx =  account.sign_transaction(tx_params)
    hash  = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx = w3.eth.wait_for_transaction_receipt(hash)
    print(f"transaction receipt {tx}")
    if not tx:
        return None 

    if tx.get('status') == 1:
        return hash.hex()




def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both dev and PyInstaller bundle """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    file_path = filedialog.askopenfilename(filetypes=[("csv file", "*.csv")])

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
            
            

def start_transactions(token_address):
    global data
    
    try:
        if data:
            print(f'the token address is {token_address}')
            if token_address != '' and str(token_address).lower() != str('Enter contract address here...').lower():
                console_log("Starting transactions...")
                console_log(" ")
                for index, row in data:
                    from_address = wallet['address']
                    pk = wallet['private']
                    to_address = row['address']
                    amount = float(row['amount'])
                    console_log(" ")
                    console_log(f"Transaction processing for...\nAddress: {to_address}\nAmount: {amount}")
                    tnx =  send_token(to_address, amount, from_address, pk,token_address)
                    if tnx:
                        status = 'successful'
                        console_log(f"Transactions completed.for address{to_address}!. status: {status}")
                        console_log(" ")
                    else:
                        status = 'failed!'
                        console_log(f"Transactions aborted! for address{to_address},check your balance and try again. status: {status}")
                        console_log(" ")
            else:
                console_log("Please enter your contract address!")
                
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
        # home_dir = os.getcwd()
        # wallet_path = os.path.join(home_dir, "core/wallet.json")
        wallet_path = resource_path("core/wallet.json")
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
                console_log("Click the 'clear' button to clear the screen when done!")
                clear_btn = tk.Button(left_frame, text="Clear", command=clear_console)
                clear_btn.pack(pady=10,padx=2)
        else:
            os.makedirs(os.path.dirname(wallet_path), exist_ok=True)
            empty_data = {}
            with open(wallet_path, 'w') as f:
                 json.dump(empty_data, f)
            
            console_log("New user,please wait while we are generating new wallet...")
            wallet = create_wallet()
            console_log("Wallet generating successful...")
            console_log("please write down your wallet details and keep it safe")
            console_log(" ")
            console_log(f"private key:{wallet['private']}")
            console_log(" ")
            console_log(f"address:{wallet['address']}")
            console_log(" ")
            console_log("Click the 'clear' button to clear the screen when done!")
            clear_btn = tk.Button(left_frame, text="Clear", command=clear_console)
            clear_btn.pack(pady=10,padx=2)
            
    except Exception as err:
        print(err)
        console_log(f"error occur:{err}")
        
        

    
def exit():
     root.destroy()
     root.quit()
     
     
def set_placeholder(entry, placeholder_text):
    placeholder_font = ("arial", 11, "normal")
    normal_font = ("arial", 11) 

    entry.insert(0, placeholder_text)
    entry.config(foreground='grey', font=placeholder_font)

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(foreground='black', font=normal_font)

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(foreground='grey', font=placeholder_font)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)




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
    token_address=ttk.Entry(left_frame,font=("arial",17,"bold"))
    token_address.pack(pady=10, fill=tk.X)
    print(token_address.get())
    set_placeholder(token_address, "Enter contract address here...")
    connect_button = tk.Button(left_frame, text="Wallet details", command=wallet_details)
    connect_button.pack(pady=10, fill=tk.X)
    # connect_button.bind("<Enter>", on_enter)
    # connect_button.bind("<Leave>", on_leave)

    upload_button = tk.Button(left_frame, text="Upload CSV", command=upload_csv)
    upload_button.pack(pady=10, fill=tk.X)
    start_button = tk.Button(left_frame, text="Start Transactions", command=lambda:start_transactions(token_address.get()))
    start_button.pack(pady=10, fill=tk.X)
    # start_button.bind("<Enter>", on_enter)
    # start_button.bind("<Leave>", on_leave)
    
    connect_button = tk.Button(left_frame, text="Exit", command=exit)
    connect_button.pack(pady=10)
    account_generation()
    root.mainloop()
    
    

    
