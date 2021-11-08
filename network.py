
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

    native_bal_raw = web3.eth.getBalance(addr)
    native_balance = web3.fromWei(native_bal_raw, "ether")

    contract_bal_raw = contract.functions.balanceOf(addr).call()
    contract_balance = web3.fromWei(contract_bal_raw, "ether")
    return native_balance,contract_balance

def estimate_gas(unsigned_txn,sender,contract=False):
    if contract == True:
        data = unsigned_txn['data']
        gas = web3.eth.estimateGas({
            "from": sender,
            "data": data,
            "to": p.contract_addr
        })
    else:
        gas = web3.eth.estimateGas(unsigned_txn)

    return gas

def create_native_txn(sender,recipient,amount):
    tx = {
        'chainId': web3.eth.chainId,
        'nonce': web3.eth.getTransactionCount(sender),
        'to':recipient,
        'value': web3.toWei(amount,'ether'),
        'gas' : 21000,
        'gasPrice': web3.toWei(30,'gwei')
    }
    return tx
def create_contract_txn(sender, recipient, amount):
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
        'gasPrice': web3.toWei(30, "gwei"),
        'nonce': nonce,
    })

    data = contract_txn['data']
    gas = web3.eth.estimateGas({
        "from": sender,
        "data": data,
        "to": p.contract_addr
    })

    contract_txn['gas'] = estimate_gas(contract_txn,sender,contract=True)

    return contract_txn

def sign_txn(priv_key, unsigned_txn):

    signed_txn = web3.eth.account.sign_transaction(unsigned_txn,private_key=priv_key)
    hashed_txn = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.toHex(hashed_txn)

def pass_contract_txn(sender_priv,sender,recipient, amount,contract=False):
    '''
    Fully passes a contract txn
    :return: True, hased_txn if passed
             False, error_message  if failed
    '''
    if (amount > float(get_bal(sender)[0])) and contract==False:
        return False, "Insufficient balance"

    if((amount > float(get_bal(sender)[1])) and (contract==True)):
        return False, "Insufficient balance"

    try:
        if (contract==True):
            unsigned_txn = create_contract_txn(sender,recipient,amount)
        elif (contract==False):
            unsigned_txn = create_native_txn(sender,recipient,amount)
        try:
            signed_txn = sign_txn(sender_priv,unsigned_txn)
            return True,signed_txn
        except Exception as e:
            return False, e

    except Exception as e:
        return False, e

