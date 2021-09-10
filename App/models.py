from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import hashlib,json
from .utils import sendTransaction
# Create your models here.

class Auctions(models.Model):
    #auction status
    active = models.BooleanField(default=True)
    #object
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    objectsName = models.CharField(max_length=20)
    startingPrice = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='media', null=True)
    descriptiveText = models.TextField()
    publicDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now_add=False)
    #bid
    lastBidder = models.CharField(max_length=20, default='')
    bid = models.IntegerField(null=True)
    lastBid = models.IntegerField(null=True, default=0)
    winner = models.CharField(max_length=20,null=True)
    #Ropsten
    hash = models.CharField(max_length=32)
    txId = models.CharField(max_length=66)

    def get_url(self):
        return reverse('bid', kwargs={'pk': self.pk})

    def auctionWinner(self):
        self.active = False
        self.winner = self.lastBidder
        actionsData = {
            'winner': self.winner,
            'paid': self.lastBidder,
            'object': self.objectsName,
        }
        jsonAcutionsData = json.dumps(actionsData)
        self.save()
        return jsonAcutionsData


    def writeOnChain(self):
        self.hash = hashlib.sha256(self.auctionWinner().encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()



