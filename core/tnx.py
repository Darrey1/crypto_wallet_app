from web3 import Web3
from eth_account import Account
import json
import asyncio
from mnemonic import Mnemonic
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

# url = "https://mainnet.infura.io/v3/bbba4fc3c0b7452ea2e46a6316da1321"
url = "https://sepolia.infura.io/v3/793c20d604d74e1f9f6aa2a8d249f226"

w3 = Web3(Web3.HTTPProvider(url))



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