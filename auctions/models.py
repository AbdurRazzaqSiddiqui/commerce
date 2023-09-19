from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.conf import settings

class User(AbstractUser):
    pass

class Auction_Listing(models.Model):
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="auctioner")
    category = models.ForeignKey('Category', blank=False, on_delete=models.CASCADE, related_name="listing_category")
    listing_name = models.CharField(max_length=50, blank=False)
    image = models.URLField(max_length=200)
    start_bid = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    highest_bid = models.ForeignKey('Bid', default=None, blank=True,null=True, on_delete=models.SET_NULL, related_name="listing_highest_bid")
    description = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing_name} in {self.category} with starting price at ${self.start_bid}"

class Bid(models.Model):
    user = models.ForeignKey(User,default=None, on_delete=models.CASCADE,related_name="bidder",editable=False)
    listing_reference = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, default=None, related_name="listing_bids")
    bidding = models.DecimalField(blank=False,max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user} bids ${self.bidding} to {self.listing_reference}"

class Comment(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE, related_name="commentator")
    listing_reference = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, default="", related_name="listing_comments")
    comment = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} comments to {self.listing_reference}"

class Watchlist(models.Model):
    user = models.ForeignKey(User,default=None,on_delete=models.CASCADE, related_name="watchlist")
    listing_reference = models.ManyToManyField(Auction_Listing, default=None, related_name="listing_watchlist")

    def __str__(self):
        return f"{self.user} Watchlist"


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False)
    listing_reference = models.ManyToManyField(Auction_Listing, default=None, related_name="category_listings")
    
    def __str__(self):
        return f"{self.category_name}"

class AuctionForm(ModelForm):
    class Meta:
        model = Auction_Listing
        fields = "__all__"
        exclude = ['user','highest_bid',]

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bidding']