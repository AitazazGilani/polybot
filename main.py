import discord
from discord.ext import commands

import setup as S
import network as n
import parse_settings as p

client = commands.Bot(command_prefix='!',help_command=None)
S.create_db()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

@client.command()
async def web3(ctx,arg):
    '''
    check if web3 connection is live
    '''
    if arg == 'status':
        test = n.test_connection()
        if test == True:
            await ctx.send("Live!")
        else:
            await ctx.send("Offline")


@client.command()
async def generate(ctx):
    '''
    Create a wallet for the user who calls the command
    '''
    acc = S.create_account()
    if S.fetch_user(ctx.author.id) == []:
        S.add_user(ctx.author.id,acc.address,S.to_hex(acc.privateKey))
        await ctx.send("your address: "+ str(acc.address))
    else:
        await ctx.send("your wallet has already been created")


#!send value ticker @username
@client.command()
async def send(ctx,arg1,arg2,*,user: discord.User=None):
    '''
    Pass a transaction, shows whether if it passed or failed in an embed
    call example: !send value ticker @username
    '''
    #check if user exists in the db
    if S.check_user(user.id) == False:
        await ctx.send("Given user does not have a wallet created")
        return

    if S.check_user(ctx.author.id) == False:
        await ctx.send("You do not have a wallet created")
        return

    val, ticker, recipient = arg1, arg2, user.id
    try:
        val = float(val)
    except:
        await ctx.send("Invalid amount given")
        return

    ticker = ticker.upper()
    recep_info = S.fetch_user(recipient)[0]
    donor_info = S.fetch_user(ctx.author.id)[0]

    addressA, privA = donor_info[1], donor_info[2]
    addressB = recep_info[1]

    #sending from addressA --> addressB
    if (ticker == "COOM"):  #If a contract token is being asked for a txn
        c = True
    elif (ticker == "MATIC"):
        c = False
    else:
        await ctx.send(f"Invalid ticker: {ticker}")
        return

    reciept = n.pass_contract_txn(privA,addressA,addressB,val,contract=c)

    if (reciept[0] == True):    #Txn was successful

        embed = discord.Embed(
            title="Transaction Successful",
            description=f"{ctx.author.mention} sent {val} {ticker} to {user.mention}",
            color=discord.Color.green()
        )

        embed.add_field(name="Reciept", value=f"https://polygonscan.com/tx/{reciept[1]}",
                        inline=False)

        await ctx.send(embed=embed)

    else:       #txn failed
        embed = discord.Embed(
            title="Transaction Failed",
            description=f"Could not sent {val} {ticker} to {user.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=f"{reciept[1]}",
                        inline=False)
        await ctx.send(embed=embed)


@client.command(name='get-uid')
async def get_uid(ctx, *, user: discord.User=None):
    '''
    get a persons uid
    '''
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
            await ctx.send("wallet has already been created")
    else:
        await ctx.send("command reserved for admins")

@client.command()
async def help(ctx):
    await ctx.send("```Commands:\n"
                   "!ping, replies with pong!\n"
                   "!web3 status, checks if connection to the node is working\n"
                   "!generate, creates an Ethereum wallet\n"
                   "!balance, get the balance of the contracts token for that user\n"
                   "!address, gets the users current Ethereum address\n"
                   "!send <value> <ticker> @username, send a person an X amount of tokens from your wallet\n"
                   "!help, replies with this text```")

@client.command()
async def balance(ctx):
    user = S.fetch_user(ctx.author.id)[0]  # holds (uid,wallet address,privkey)

    check = S.check_user(ctx.author.id)  # check if wallet exists correct

    if check == False:
        await ctx.send("You do not have any active wallets")
    else:
        embed = discord.Embed(
            title="Balance",
            description=ctx.author.mention,
            color = discord.Color.orange()
        )
        embed.add_field(name="Polygon", value=str(n.get_bal(user[1])[0])+"  <:polygon:906994678367391754>",inline=False)
        embed.add_field(name = "CumDogeElonPussyShit coin", value = str(n.get_bal(user[1])[1])+"  <:coomer:881353486296580176>")
        embed.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed=embed)

@client.command()
async def address(ctx):
    user = S.fetch_user(ctx.author.id)[0]  # holds uid,wallet address, privkey

    check = S.check_user(ctx.author.id)  # check if wallet exists
    if check == False:
        await ctx.send("You do not have any active wallets")
    else:
        embed = discord.Embed(
            title="Address",
            description=ctx.author.mention,
            color=discord.Color.orange()
        )
        embed.add_field(name="Ethereum address", value=user[1])

        embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
client.run(p.bot_id)
