import web3
from web3 import Web3

w3 = Web3(web3.HTTPProvider('https://ropsten.infura.io/v3/534a6ba32faa49eab8f59a336a9fe7e3'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"your address: {address} \nYour Key: {privateKey}")