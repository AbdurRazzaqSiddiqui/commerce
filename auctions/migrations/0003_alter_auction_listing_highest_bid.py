# Generated by Django 4.2 on 2023-08-21 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_listing_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='highest_bid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listing_highest_bid', to='auctions.bid'),
        ),
    ]
