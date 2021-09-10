# Generated by Django 3.2.7 on 2021-09-10 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('objectsName', models.CharField(max_length=20)),
                ('startingPrice', models.PositiveIntegerField(null=True)),
                ('image', models.ImageField(null=True, upload_to='media')),
                ('descriptiveText', models.TextField()),
                ('publicDate', models.DateTimeField(auto_now_add=True)),
                ('endDate', models.DateTimeField()),
                ('lastBidder', models.CharField(default='', max_length=20)),
                ('bid', models.IntegerField(null=True)),
                ('lastBid', models.IntegerField(default=0, null=True)),
                ('winner', models.CharField(max_length=20, null=True)),
                ('hash', models.CharField(max_length=32)),
                ('txId', models.CharField(max_length=66)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
