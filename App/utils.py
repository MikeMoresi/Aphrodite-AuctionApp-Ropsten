from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/534a6ba32faa49eab8f59a336a9fe7e3'))
    address = '0xdaa3629e53b8c38a038C80F038F45516A629f4A1'
    privateKey = '0x35e9851836d669810541feb33100d6ad5df8eeb1799b67d52263fe75226f5eb4'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0,'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ),privateKey)

    tx= w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId