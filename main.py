import discord
from discord.ext import commands

import setup as S
import network as n
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def web3(ctx,arg):
    if arg == 'status':
        test = n.test_connection()
        if test == True:
            await ctx.send("Live!")
        else:
            await ctx.send("Offline")


@client.command()
async def generate(ctx,arg):
    if arg == 'wallet':
        acc = S.create_account() #need to make a data base for the user here
        await ctx.send(acc.address)

@client.command()
async def get(ctx,*args):
    if args[0] == 'balance':
        user_adr = str(args[1]) #holds wallet address
        # check if wallet is correct
        check = n.check_addr(user_adr)
        if check == True:
            balance = n.get_bal(user_adr)
            await ctx.send(str(balance) + " ETH")
        else:
            await ctx.send("address not found")
#!send value addr1 privkey(addr1) addr2
@client.command()
async def send(ctx,*args):
    value = args[0]
    try: #check if given value is a number
        value = float(value)
    except:
        await ctx.send("invalid amount of eth to be transacted")
    addr_1 = args[1]
    priv = args[2]
    addr_2 = args[3]

    if (n.check_addr(addr_1) == False) or (n.check_addr(addr_2) == False) :
        await ctx.send("invalid address given")

    if n.get_bal(addr_1) < value:
        await ctx.send("insufficient balance")

    tx = n.transaction()
    tx.addrA = addr_1
    tx.addrB = addr_2
    tx.value = value
    tx.gasPrice = 20000000000
    tx_data = tx.create_dict()
    tx_signed = tx.sign_transaction(tx_data,priv)
    tx_hashed = tx.ex_rawTx(tx_signed)

    tx_confirm = tx.hex_tx(tx_hashed)

    await ctx.send("Transactions successful\n Contract Address: " + tx_confirm)







client.run('ODU1MjI1MDUzMDIwNTUzMjM2.YMvYZQ.VaBz5KJ2bn4-ignx0ilGJgdK17k')
