import discord
from web3 import Web3
import setup as S
client = discord.Client()

url = "https://rpc-mainnet.maticvigil.com/v1/b20459a39192d4978e017db439b3a37d314059ae"
web3 = Web3(Web3.HTTPProvider(url))

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('Pong')

    if message.content.startswith('$web3 polygon status'):
        test = web3.isConnected()
        if test == True:
            await message.channel.send('Live!')
        else:
            await message.channel.send('Connection offline')

    if message.content.startswith('$generate wallet'):
        account1 = S.create_account()
        await message.channel.send(str(account1.address))
client.run('ODU1MjI1MDUzMDIwNTUzMjM2.YMvYZQ.VaBz5KJ2bn4-ignx0ilGJgdK17k')
