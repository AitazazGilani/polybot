
from web3 import Web3
import parse_settings as p


web3 = Web3(Web3.HTTPProvider(p.rpc))
contract = web3.eth.contract(address=p.contract_addr,abi=p.abi)


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
        'chainId': web3.eth.chainId,
        'gas': 0,
        'gasPrice': web3.toWei(50, "gwei"),
        'nonce': nonce,
    })

    data = contract_txn['data']
    gas = web3.eth.estimateGas({
        "from": sender,
        "data": data,
        "to": p.contract_addr
    })

    contract_txn['gas'] = gas

    return contract_txn

def sign_txn(priv_key, contract_txn):

    signed_txn = web3.eth.account.sign_transaction(contract_txn,private_key=priv_key)
    hashed_txn = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.toHex(hashed_txn)


