# Generated by Django 3.2.7 on 2021-09-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_auction_selleraddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='sellerAddress',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]