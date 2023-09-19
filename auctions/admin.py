from django.contrib import admin
from .models import Auction_Listing, Bid, Category, User, Comment, Watchlist

# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("user","category","listing_name","image","start_bid","description")
    # filter_horizontal = ("bids",)

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("listing_refernece")

class BidAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            obj = Bid.objects.get(user=request.user)
            # If Found
            raise ValueError("Current user has already bid on the this listing.")
        except:
            obj.user = request.user
            super().save_model(request, obj, form, change)
            
        
admin.site.register(Auction_Listing,AuctionAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Watchlist)