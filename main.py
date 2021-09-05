import discord
from discord.ext import commands

import setup as S
import network as n
client = commands.Bot(command_prefix='!')
#S.create_db()

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
        acc = S.create_account()
        if S.fetch_user(ctx.author.id) == []:
            S.add_user(ctx.author.id,acc.address,acc.privateKey)
            await ctx.send("your address:",acc.address)
        else:
            await ctx.send("your wallet has already been created")

@client.command()
async def get(ctx,*args):
    if args[0] == 'balance':
        user = S.fetch_user(ctx.author.id) #holds wallet address
        # check if wallet is correct
        check = user
        if check == []:
            await ctx.send("You do not have any active wallets")
        else:
            balance = n.get_bal(user[1])
            await ctx.send('{} {}'.format(balance,'COOM'))


#!send value ticker addr1 privkey(addr1) addr2
#!send value ticker @username
@client.command()
async def send(ctx,*args):
    value = args[0]
    try: #check if given value is a number
        value = float(value)
    except:
        await ctx.send("invalid amount of COOM to be transacted")
    addr_1 = args[2]
    priv = args[3]
    addr_2 = args[4]

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

@client.command()
async def user(ctx):
    await ctx.send(ctx.author.id)

@client.command(name='get-uid')
async def get_uid(ctx, *, user: discord.User=None):
    if user != None:
        await ctx.send(f'{user.id}')
    else:
        await ctx.send('user not found')

client.run('ODU1MjI1MDUzMDIwNTUzMjM2.YMvYZQ.VaBz5KJ2bn4-ignx0ilGJgdK17k')
