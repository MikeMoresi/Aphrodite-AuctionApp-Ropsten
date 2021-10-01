from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SellForms, BidForms, TokenBidForms
from .models import Auction
from django.contrib import messages
from .filters import AuctionFilter
import redis, datetime, web3
from web3 import Web3

# redis
client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=None, decode_responses=True)
# connection to Aphrodite smart contract
# ERC-20 token mined is aUSD, suppose 1 USD = 1 aUSD
w3 = Web3(web3.HTTPProvider('https://ropsten.infura.io/v3/534a6ba32faa49eab8f59a336a9fe7e3'))
contractAddress = '0xeD47A3870DF0a2cE32947B1482bB6BCce25419b1'
abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            }
        ],
        "name": "allowance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "account",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "subtractedValue",
                "type": "uint256"
            }
        ],
        "name": "decreaseAllowance",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "spender",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "addedValue",
                "type": "uint256"
            }
        ],
        "name": "increaseAllowance",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "sender",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
aphroditeContract = w3.eth.contract(address=contractAddress, abi=abi)
contractOwner = '0x0A21EF3B600f508C6A9d1Acd11A0F3fC853475b1'



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def mainpage(request):
    objects = Auction.objects.filter(active=True).order_by('endDate')
    for obj in objects:
        # when the current date is equal to endDate
        if obj.endDate.replace(tzinfo=None) <= datetime.datetime.now():
            #if no one has made any offers
            if obj.lastBidder is None:
                obj.active = False
                obj.save()
            else:
                # write auction data on json
                obj.auctionWinner()
                # send to ropsten
                obj.writeOnChain()
                # pay the seller
                if obj.sellerAddress != None:
                    tx_hash = aphroditeContract.functions.transfer(obj.sellerAddress, int(obj.price)).transact({'from': contractOwner})
                    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    rich_logs = aphroditeContract.events.Transfer().processReceipt(tx_receipt)
                    sellerEvent = rich_logs[0]['args']
                    client.lpush('lSellerEvent', str(sellerEvent))
                    # refund losing bidders
                    losers = obj.lbidderAddress[:-1]
                    for i in losers:
                        for loserAddress,loserBid in i.items():
                            tx_hash = aphroditeContract.functions.transfer(loserAddress, int(loserBid)).transact({'from': contractOwner})
                            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                            rich_logs = aphroditeContract.events.Transfer().processReceipt(tx_receipt)
                            loserEvent = rich_logs[0]['args']
                            client.lpush('lLoserEvent',str(loserEvent))

    # add a filter to search for item
    myFilter = AuctionFilter(request.GET, queryset=objects)
    objects = myFilter.qs

    return render(request, 'mainpage.html', {'objects': objects, 'myFilter': myFilter,})


def sellView(request):
    if request.method == "POST":
        form = SellForms(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            now = datetime.datetime.now()
            # check if the endDate is correct
            if auction.endDate.replace(tzinfo=None) <= now:
                messages.error(request, 'Today is ' + str(now.strftime("%m/%d/%Y - %H:%M:%S")) + '!')
                return redirect(reverse('sell'))
            if auction.sellerAddress == None:
                auction.save()
                return redirect(reverse('mainpage'))
            else:
                # check if the sellerAddress is correct
                if Web3.isAddress(auction.sellerAddress) != True:
                    messages.error(request, 'Invalid address')
                    return redirect(reverse('sell'))
                auction.save()
                return redirect('mainpage')
    else:
        form = SellForms()
    return render(request, 'sell.html', {'form': form})

# bid in USD
def bidView(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    user = request.user
    form = BidForms(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            bid = request.POST.get('bid')

            # check bidder data
            if float(bid) <= 0:
                messages.error(request, 'Invalid Offer')
                return redirect(reverse('bid', kwargs={'pk': auction.pk}))
            if float(bid) <= auction.price:
                messages.error(request, 'Your offer has to be greater than the current one!')
                return redirect(reverse('bid', kwargs={'pk': auction.pk}))
            if user == auction.lastBidder:
                messages.error(request, 'You are already the higthest bidder!')
                return redirect(reverse('bid', kwargs={'pk': auction.pk}))
            if user == auction.seller:
                messages.error(request, 'You can t bid on your own product!')
                return redirect(reverse('bid', kwargs={'pk': auction.pk}))

            # save
            messages.success(request, 'Well done, your offer has been saved!')
            auction.lastBidder = user
            auction.price = bid
            client.lpush('lBid', auction.price, str(auction.lastBidder), str(pk))
            auction.save()
            return redirect('mainpage')

        else:
            form = BidForms()
    return render(request, 'bid.html', {'form': form, 'auction': auction})

# bid in aUSD
def tokenBidView(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    user = request.user
    form = TokenBidForms(request.POST)

    # ERC-20 token mined is aUSD, suppose 1 USD = 1 aUSD
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            bid = request.POST.get('bid')
            bidderAddress = request.POST.get('bidderAddress')
            # bidder address check
            if Web3.isAddress(bidderAddress) != True:
                messages.error(request, 'Your address is not valid!')
                return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))
            if aphroditeContract.functions.balanceOf(bidderAddress).call() < float(bid):
                messages.error(request, 'your bid exceeds your balance')
                return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))
            else:
                # check bidder data
                if float(bid) <= 0:
                    messages.error(request, 'Invalid Offer')
                    return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))
                if float(bid) <= auction.price:
                    messages.error(request, 'Your offer has to be greater than the current one!')
                    return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))
                if user == auction.lastBidder:
                    messages.error(request, 'You are already the higthest bidder!')
                    return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))
                if user == auction.seller:
                    messages.error(request, 'You can t bid on your own product!')
                    return redirect(reverse('tokenBid', kwargs={'pk': auction.pk}))

                # send bid transaction from bidder to contractOwner
                tx_hash = aphroditeContract.functions.transfer(contractOwner, int(bid)).transact({'from': bidderAddress})
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                rich_logs = aphroditeContract.events.Transfer().processReceipt(tx_receipt)
                event = rich_logs[0]['args']

                # save
                messages.success(request, 'Well done, your offer has been saved!')
                # we create a list of dict with bidder address and bid in order to use it in mainpage view and refund the losers
                dictBidderAddress = {bidderAddress:bid}
                auction.lbidderAddress.append(dictBidderAddress)
                auction.lastBidder = user
                auction.price = bid
                client.lpush('lBid', auction.price, str(auction.lastBidder), str(pk), str(event))
                auction.save()
                return redirect('mainpage')

        else:
            form = TokenBidForms()
    return render(request, 'tokenBid.html', {'form': form, 'auction': auction})

