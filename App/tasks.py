from background_task import background
import redis,hashlib,time
from .utils import sendTransaction


client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=None, decode_responses=True)

@background()
def writeRedisBidDataOnChain():
        bidOnRedis = client.lrange('lBid',0,-1)
        bidOnRedisHash = hashlib.sha256(str(bidOnRedis).encode('utf-8')).hexdigest()
        a = sendTransaction(bidOnRedisHash)
        hours = 24
        minutes = 60 * hours
        seconds = 60 * minutes
        time.sleep(10)

