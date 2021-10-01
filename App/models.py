from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import hashlib,json
from .utils import sendTransaction
# Create your models here.


class Auction(models.Model):
    #auction status
    active = models.BooleanField(default=True)
    #object
    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name='seller')
    sellerAddress = models.CharField(max_length=256,blank=True,null=True)
    title = models.CharField(max_length=20)
    price = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='media', null=True)
    descriptiveText = models.TextField()
    publicDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now_add=False)
    #bid
    bidderAddress = models.CharField(max_length=256,null=True)
    lbidderAddress = models.JSONField(default=list)
    lastBidder = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lastBid',null=True)
    bid = models.IntegerField(null=True)
    #Ropsten
    hash = models.CharField(max_length=32)
    txId = models.CharField(max_length=66)

    def get_url(self):
        return reverse('bid', kwargs={'pk': self.pk})

    def token_get_url(self):
        return reverse('tokenBid',kwargs={'pk': self.pk})

    def auctionWinner(self):
        self.active = False
        actionsData = {
            'winner': str(self.lastBidder),
            'paid': self.price,
            'object': self.title,
        }
        jsonAcutionsData = json.dumps(actionsData)
        self.save()
        return jsonAcutionsData


    def writeOnChain(self):
        self.hash = hashlib.sha256(self.auctionWinner().encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()

