import django_filters
from .models import *
from django_filters import DateFilter, NumberFilter, CharFilter

class AuctionFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title',lookup_expr='contains')
    pricelte = NumberFilter(field_name='price',lookup_expr='lte')
    pricegte = NumberFilter(field_name='price',lookup_expr='gte')
    enddatelte = DateFilter(field_name='endDate',lookup_expr='lte')
    enddategte = DateFilter(field_name='endDate',lookup_expr='gte')


    class Meta:
        model = Auction
        exclude = ('active','image','hash','txId','lastBidder','descriptiveText','bid','publicDate','endDate','price','title')
        fields = ('seller',)
