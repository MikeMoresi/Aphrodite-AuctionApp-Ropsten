# Generated by Django 3.2.7 on 2021-09-28 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_rename_selleraddress_auction_bidderaddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='priceInToken',
        ),
    ]