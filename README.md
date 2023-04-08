# polybot
An Ethereum wallet for discord

A python based discord bot that takes in commands in terms of text messages sent on discord and lets the user send ERC-20 transactions to other users on discord. 

# Key functionality:
 * Create and Store wallet addresses and keys for users in a SQL db
 * Add custom rpc's and connections to Ethereum based blockchains (Avalanche, Polygon, Fantom, etc)
 * Send native token and custom token transactions between users as defined 

# Requirments:
 * Python 3.8
 * Discord.py
 * Web3.py (follow instructions on Web3.py documentation for further required dependancies) 
 * SQLite3 for python
  

To deploy:
 * Log in to discord developers portal, create a new bot and set the approprite permissions (read and write messages)
 * Copy the api key from developers portal and insert the api key into main.py
 * Run Main.py
