from django import forms
from .models import Auction

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class SellForms(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('title','image','price','descriptiveText','endDate','sellerAddress')
        labels = {'title':'Title','startingPrice':'Which is your item first price?','descriptiveText':'Describe your Item','endDate':'Auction End Date','sellerAddress':'OPTIONAL: Ethereum Address'}
        widgets = {'endDate': DateTimeInput()}

class BidForms(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('bid',)

class TokenBidForms(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('bidderAddress','bid',)
        labels = {'bidderAddress':'Your Address'}






