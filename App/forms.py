from django import forms
from .models import Auctions

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class SellForms(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ('objectsName','image','startingPrice','descriptiveText','endDate')
        labels = {'objectsName':'Title','startingPrice':'Which is your item first price?','descriptiveText':'Describe your Item','endDate':'Auction End Date'}
        widgets = {'endDate': DateTimeInput()}

class BidForms(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ('bid',)






