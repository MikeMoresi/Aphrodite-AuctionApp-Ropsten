from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import hashlib,json,redis,time
from .utils import sendTransaction
# Create your models here.


class Auction(models.Model):
    #auction status
    active = models.BooleanField(default=True)
    #object
    seller = models.ForeignKey(User, on_delete=models.CASCADE,related_name='seller')
    title = models.CharField(max_length=20)
    price = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='media', null=True)
    descriptiveText = models.TextField()
    publicDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField(auto_now_add=False)
    #bid
    lastBidder = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lastBid',null=True)
    bid = models.IntegerField(null=True)
    #Ropsten
    hash = models.CharField(max_length=32)
    txId = models.CharField(max_length=66)

    def get_url(self):
        return reverse('bid', kwargs={'pk': self.pk})

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

    def writeRedisOnChain(self):
        while (1):
            client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=None, decode_responses=True)
            bidOnRedis = str(client.lrange('lBid', 0, -1))
            bidOnRedisHash = hashlib.sha256(bidOnRedis.encode('utf-8')).hexdigest()
            a = sendTransaction(bidOnRedisHash)
            print(a)
            hours = 24
            minutes = 5
            seconds = 60 * minutes
            time.sleep(seconds)



