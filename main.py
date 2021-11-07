import discord
from discord.ext import commands

import setup as S
import network as n
import parse_settings as p

client = commands.Bot(command_prefix='!')
S.create_db()

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
async def generate(ctx):
    acc = S.create_account()
    if S.fetch_user(ctx.author.id) == []:
        S.add_user(ctx.author.id,acc.address,S.to_hex(acc.privateKey))
        await ctx.send("your address: "+ str(acc.address))
    else:
        await ctx.send("your wallet has already been created")

@client.command()
async def get(ctx,*args):
    user = S.fetch_user(ctx.author.id)  # holds wallet address
    # check if wallet is correct
    check = user
    if args[0] == 'balance':
        if check == []:
            await ctx.send("You do not have any active wallets")
        else:
            balance = n.get_bal(user[0][1])
            await ctx.send('{} {}'.format(balance,'COOM'))
    elif (args[0] == 'address'):
        if check!=[]:
            user = S.fetch_user(ctx.author.id)
            await ctx.send("Your address: " + str(user[0][1]))
        else:
            await ctx.send("You do not have any active wallets")



#!send value ticker addr1 privkey(addr1) addr2
#!send value ticker @username
@client.command()
async def send(ctx,arg1,arg2,*,user: discord.User=None):
    val = arg1
    ticker = arg2
    recipient = user.id

    try:
        val = int(val)
    except:
        await ctx.send("invalid amount of coom given")

    ticker = ticker.upper()
    if ticker != "COOM":
        ctx.send("invalid ticker")

    recep_info = S.fetch_user(recipient)
    donor_info = S.fetch_user(ctx.author.id)

    if recep_info == []:
        await ctx.send("Given user does not have a wallet created")
    elif donor_info == []:
        await ctx.send("You do not have a wallet created")
    else:
        addressA = donor_info[0][1]
        pkeyA = donor_info[0][2]
        addressB = recep_info[0][1]
        user_txn = n.create_txn(addressA,addressB,val)
        reciept = n.sign_txn(pkeyA,user_txn)
        await ctx.send(f"Transaction reciept: https://polygonscan.com/tx/{reciept}")

@client.command()
async def user(ctx):
    await ctx.send(ctx.author.id)

@client.command(name='get-uid')
async def get_uid(ctx, *, user: discord.User=None):
    if user != None:
        await ctx.send(f'{user.id}')
    else:
        await ctx.send('user not found')

@client.command(name='make-wallet')
async def make(ctx,*,user: discord.User=None):
    if ctx.author.id == 340751508138229762:
        acc = S.create_account()
        if S.fetch_user(user.id) == []:
            S.add_user(user.id,acc.address,S.to_hex(acc.privateKey))
            await ctx.send("your address: "+ str(acc.address))
        else:
            await ctx.send("your wallet has already been created")
    else:
        await ctx.send("command reserved for admins")


client.run(p.bot_id)
