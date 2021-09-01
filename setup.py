#file used for creating first time data and data bases for new users

from web3 import Web3, Account
import secrets

def create_account():
    '''
    create an ethereum wallet
    :returns: an object class containing info about the account
    such as wallet address, private key, etc
    '''
    private_key = "0x" + secrets.token_hex(32)
    acct = Account.from_key(private_key)
    return acct



