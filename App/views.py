from django.shortcuts import render,redirect, get_object_or_404,reverse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import SellForms,BidForms
from .models import Auction
from django.contrib import messages
from .filters import AuctionFilter
import redis, datetime



#redis
client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=None, decode_responses=True)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def mainpage(request):
    objects = Auction.objects.filter(active=True).order_by('endDate')
    for obj in objects:
        if obj.endDate.replace(tzinfo=None) <= datetime.datetime.now():
            if obj.lastBidder is None:
                obj.active = False
                obj.save()
            else:
                # write auction data on json
                obj.auctionWinner()
                #send to ropsten
                obj.writeOnChain()

    myFilter = AuctionFilter(request.GET, queryset=objects)
    objects = myFilter.qs

    return render(request,'mainpage.html',{'objects':objects,'myFilter':myFilter})

def sellView(request):
    if request.method == "POST":
        form = SellForms(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            now = datetime.datetime.now()
            if auction.endDate.replace(tzinfo=None) <= now:
                messages.error(request, 'Today is ' + str(now.strftime("%m/%d/%Y - %H:%M:%S")) + '!')
                return redirect(reverse('sell'))
            auction.save()
            return redirect('mainpage')
    else:
        form = SellForms()
    return render(request, 'sell.html', {'form': form})


def bidView(request,pk):
    auction = get_object_or_404(Auction,pk=pk)
    user = request.user
    form = BidForms(request.POST)
    if request.method == 'POST':
        if form.is_valid():
                form = form.save(commit=False)
                bid = request.POST.get('bid')

                #control
                if float(bid) <= 0:
                    messages.error(request,'Invalid Offer')
                    return redirect(reverse('bid',kwargs={'pk':auction.pk}))
                if float(bid) <= auction.price:
                    messages.error(request, 'Your offer has to be greater than the current one!')
                    return redirect(reverse('bid', kwargs={'pk': auction.pk}))
                if user == auction.lastBidder:
                    messages.error(request, 'You are already the higthest bidder!')
                    return redirect(reverse('bid', kwargs={'pk': auction.pk}))
                if user == auction.seller:
                    messages.error(request, 'You can t bid on your own product!')
                    return redirect(reverse('bid', kwargs={'pk': auction.pk}))

                #save
                messages.success(request,'Well done, your offer has been saved!')
                auction.lastBidder = user
                auction.price = bid
                client.lpush('lBid', auction.price, str(auction.lastBidder), str(pk))
                auction.save()
                return redirect('mainpage')

        else:
            form = BidForms()
    return render(request,'bid.html',{'form':form,'auction':auction})




