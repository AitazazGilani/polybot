
#using polygon by default
import json
from web3 import Web3

url = "https://rpc-mainnet.maticvigil.com/v1/b20459a39192d4978e017db439b3a37d314059ae"
web3 = Web3(Web3.HTTPProvider(url))
abi = json.loads('[{"inputs": [{"internalType": "uint256","name": "initialSupply","type": "uint256"}],"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "address","name": "spender","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "from","type": "address"},{"indexed": true,"internalType": "address","name": "to","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Transfer","type": "event"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "spender","type": "address"}],"name": "allowance","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "approve","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "account","type": "address"}],"name": "balanceOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "decimals","outputs": [{"internalType": "uint8","name": "","type": "uint8"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "subtractedValue","type": "uint256"}],"name": "decreaseAllowance","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "addedValue","type": "uint256"}],"name": "increaseAllowance","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "name","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "symbol","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "totalSupply","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transfer","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "sender","type": "address"},{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transferFrom","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"}]')
address = "0xF642254566c6A0057e11d3be36ee15eb9F8dF366"
contract = web3.eth.contract(address=address,abi=abi)
chainId = 137



def test_connection():
    '''
    check if web3 connection is live, returns a bool
    '''
    return web3.isConnected()

def check_addr(addr):
    '''
    check if a given address is valid
    :param addr: a string
    :return: bool
    '''
    #assert type(addr) == "<class 'str'>"
    return web3.isAddress(addr)

def get_bal(addr):
    '''
    get the balance of the address in wei
    :addr: a string, containing a valid eth address
    :return: a float
    '''

    rawbals = contract.functions.balanceOf(addr).call()
    bals = web3.fromWei(rawbals, "ether")
    return bals

def create_txn(sender, recipient, amount):
    '''
    Create an dictionary containg all the information needed to pass a transaction
    :sender: String, is the address of the sender
    :recipient: String, is the address of the recipient
    :amount: int, amount of the erc20 token (contract) you are sending
    '''

    nonce = web3.eth.get_transaction_count(sender)

    contract_txn = contract.functions.transfer(
        recipient,
        web3.toWei(amount, "ether"),
    ).buildTransaction({
        'chainId': chainId,
        'gas': 0,
        'gasPrice': web3.toWei(50, "gwei"),
        'nonce': nonce,
    })

    data = contract_txn['data']
    gas = web3.eth.estimateGas({
        "from": personA,
        "data": data,
        "to": address
    })

    contract_txn['gas'] = gas

    return contract_txn

def sign_txn(priv_key, contract_txn):
    try:
        signed_txn = web3.eth.account.sign_transaction(unicorn_txn,private_key=priv)
        hashed_txn = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return web3.toHex(hashed_txn)
    except(error):
        return error

