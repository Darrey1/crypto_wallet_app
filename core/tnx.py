from web3 import Web3
from eth_account import Account
import json
import asyncio
from mnemonic import Mnemonic
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

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
token_address = w3.to_checksum_address("0x59e8f13f80b405992e6db077b255a11cdba588ab")
token_contract = w3.eth.contract(address=token_address, abi = erc20_abi)
decimals = token_contract.functions.decimals().call()


def balance(address):
    get_balance = w3.eth.get_balance(w3.to_checksum_address(address))
    balance = w3.from_wei(get_balance, "ether")
    return format(float(balance),'.3f')


def create_wallet():
    wallet_path = os.path.join(script_directory, "wallet.json")
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=256)
    w3.eth.account.enable_unaudited_hdwallet_features()
    account = w3.eth.account.from_mnemonic(words)
    data = {
        "private": account.key.hex(),
        "address": account.address,
        "mnemonic": words,
    }
    with open(wallet_path, mode='w') as file:
        json.dump(data,file)
    return data


def get_wallet():
    try:
        wallet_path = os.path.join(script_directory, "wallet.json")
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


def send_token(to_ : str, amount : float | int, from_address : str, private_key : str):
    
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