import json
#imports settings.json, abi.json

#open settings.json
with open('settings.json','r') as f:
    data = json.load(f)
    bot_id = data["bot-id"]
    rpc = data["network-rpc"]
    contract_addr = data["contract-address"]
    contract_ticker = data["contract-token"]
    native_ticker = data["native-token"]

#open abi.json
with open("abi.json",'r') as f:
    wrapped_abi = ''
    for x in f:
        wrapped_abi += x
    abi = json.loads(wrapped_abi)


