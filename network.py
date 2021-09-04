#web3 connection
#file will hold the information about which network to connect to
#example: ethereum, polygon, terra, avax etc

#using polygon by default
import json
from web3 import Web3

url = "HTTP://127.0.0.1:7545"
    #"https://rpc-mainnet.maticvigil.com/v1/b20459a39192d4978e017db439b3a37d314059ae"
web3 = Web3(Web3.HTTPProvider(url))

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
    bals = web3.eth.get_balance(addr)
    bals = web3.fromWei(bals,'ether')
    return bals

class transaction(object):
    def __init__(self,addrA=None,addrB=None,value=0,gas=6721975,gasPrice=None):
        self.addrA = addrA #account we are sending money from
        self.addrB = addrB
        self.value = value
        self.gas = gas
        self.gasPrice = gasPrice

    def create_dict(self):

        tx = {
            'nonce' : web3.eth.getTransactionCount(self.addrA),
            'to': self.addrB,
            'value': web3.toWei(self.value,'ether'),
            'gas': self.gas,
            'gasPrice': web3.toWei('50','gwei')

        }
        return tx

    def sign_transaction(self , tx ,priv):
        signed_tx = web3.eth.account.sign_transaction(tx,priv)
        return signed_tx

    def ex_rawTx(self,signedTx):
        tx_hash = web3.eth.sendRawTransaction(signedTx.rawTransaction)
        return tx_hash

    def hex_tx(self,hashed_tx):
        return web3.toHex(hashed_tx)

