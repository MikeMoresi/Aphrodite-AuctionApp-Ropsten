# Generated by Django 3.2.7 on 2021-09-28 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auction_selleraddress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='sellerAddress',
            new_name='bidderAddress',
        ),
    ]