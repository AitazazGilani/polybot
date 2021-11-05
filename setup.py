#file used for creating first time data and data bases for new users
from web3 import Web3, Account
import secrets
import sqlite3
import os


def create_account():
    '''
    create an ethereum wallet
    :returns: an object class containing info about the account
    such as wallet address, private key, etc
    '''
    private_key = "0x" + secrets.token_hex(32)
    acct = Account.from_key(private_key)
    return acct

def to_hex(priv):
    return Web3.toHex(priv)


def check_db():
    '''
    check if a database exists
    :return: True if it does, false if otherwise
    '''
    return os.path.isfile('wallet_base.db')

def create_db():
    '''
    create a database, if it doesnt exist
    '''
    check = check_db()
    if check == False:
        conn = sqlite3.connect('wallet_base.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE users (
        		id text,
        		wallet text,
        		privkey text
        	)""")
        conn.commit()
        conn.close()

def add_user(username,addr,priv):
    '''
    add a user to the database
    :param id: discord id, str
    :param addr: wallet address, str
    :param priv: private key, str
    '''
    conn = sqlite3.connect('wallet_base.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES ('{}','{}','{}')".format(username,addr,priv))
    conn.commit()
    conn.close()

def fetch_user(username):
    '''
    Fetch a user from the data base
    :param username: str, the id of the table in db
    :return: a tuple containing, username, wallet address, private key
    '''
    conn = sqlite3.connect('wallet_base.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE id ='{}' ".format(username))
    info = c.fetchall()
    conn.commit()
    conn.close()

    return info

def delete_user(username):
    '''
    delete a user in the database
    '''
    conn = sqlite3.connect('wallet_base.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id ='{}' ".format(username))

    conn.commit()
    conn.close()

