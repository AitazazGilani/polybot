
from web3 import Web3,Account
import json
import network as n


url = "https://rpc-mainnet.maticvigil.com/v1/b20459a39192d4978e017db439b3a37d314059ae"
web3 = Web3(Web3.HTTPProvider(url))
abi = json.loads('[{"inputs": [{"internalType": "uint256","name": "initialSupply","type": "uint256"}],"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "address","name": "spender","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "from","type": "address"},{"indexed": true,"internalType": "address","name": "to","type": "address"},{"indexed": false,"internalType": "uint256","name": "value","type": "uint256"}],"name": "Transfer","type": "event"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "spender","type": "address"}],"name": "allowance","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "approve","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "account","type": "address"}],"name": "balanceOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "decimals","outputs": [{"internalType": "uint8","name": "","type": "uint8"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "subtractedValue","type": "uint256"}],"name": "decreaseAllowance","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "spender","type": "address"},{"internalType": "uint256","name": "addedValue","type": "uint256"}],"name": "increaseAllowance","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "name","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "symbol","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "totalSupply","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transfer","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "sender","type": "address"},{"internalType": "address","name": "recipient","type": "address"},{"internalType": "uint256","name": "amount","type": "uint256"}],"name": "transferFrom","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "nonpayable","type": "function"}]')
address = web3.toChecksumAddress("0xF642254566c6A0057e11d3be36ee15eb9F8dF366")
unicorns = web3.eth.contract(address=address,abi=abi)

personA='0x6Fe706a8643C379113B2754092DE53c8Bbd97c83'
personB = "0xae82643a4e96AAD75C599f0967F2A1B4b24c6629"
nonce = web3.eth.get_transaction_count(personA)
print("Before\nPersonA:",n.get_bal(personA))
print("Person B:",n.get_bal(personB))

unicorn_txn = unicorns.functions.transfer(
   personB,
   web3.toWei(45.55,"ether"),
 ).buildTransaction({
   'chainId': 137,
   'gas': 0,
    'gasPrice': web3.toWei(50,"gwei"),
    'nonce': nonce,
})

print(unicorn_txn)
data = unicorn_txn['data']
gas = web3.eth.estimateGas({
    "from" : personA,
    "data" : data,
    "to": address
})
unicorn_txn['gas'] = gas
print(gas)

priv =b'\xb1\x9c\xc8s3\x01\x17\x04\x93e\xb3~\xa4q\xb9z\xaa_\xcd\x9c\xdfC`W\xcf:\x01\xc9\xbb\xf3\x0c\x92'
signed_txn = web3.eth.account.sign_transaction(
    unicorn_txn
,private_key=priv)
signed_txn.rawTransaction
web3.eth.send_raw_transaction(signed_txn.rawTransaction)

print("After\nPersonA:",n.get_bal(personA))
print("Person B:",n.get_bal(personB))