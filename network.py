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

def create_transaction():
    return None



