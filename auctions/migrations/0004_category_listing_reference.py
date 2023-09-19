# Generated by Django 4.2 on 2023-08-22 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listing_highest_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='listing_reference',
            field=models.ManyToManyField(default=None, related_name='category_listings', to='auctions.auction_listing'),
        ),
    ]