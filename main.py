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

@client.command()
async def send(ctx,*args):




client.run('ODU1MjI1MDUzMDIwNTUzMjM2.YMvYZQ.VaBz5KJ2bn4-ignx0ilGJgdK17k')
