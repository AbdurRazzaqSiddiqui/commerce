from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, AuctionForm, Auction_Listing, Category, Comment, Bid, Watchlist
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "auctions/index.html",{
        "listings":Auction_Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            try:
                Watchlist.objects.get(user=request.user)
            except Watchlist.DoesNotExist:
                watchlist = Watchlist.objects.create(user=request.user)
                watchlist.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            watchlist = Watchlist.objects.create(user=request.user)
            user.save()
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='auctions:login')
def create_listing(request):
    if request.method == "POST":
        listing_name = request.POST["listing_name"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        image = request.POST["image"]
        start_bid = request.POST["start_bid"]
        description = request.POST["description"]
        Listing = Auction_Listing.objects.create(user=request.user, status=True, category=category, listing_name=listing_name, image=image, start_bid=start_bid, description=description,highest_bid=None)
        Listing.save()
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request,"auctions/create_listing.html",{
            "cat_objs":Category.objects.all()
        })

def listing(request,listing_id):
    auction_list = Auction_Listing.objects.get(id=listing_id)
    watchlist_option = False
    winner = False
    bid_option = False
    comment_option = None
    error_message = False

    # For Active Status and Winner
    if not auction_list.status:
        try:
            winner = Bid.objects.get(bidding=auction_list.highest_bid.bidding)
            winner = "This Listing has already been sold to "+str(winner.user.username)+" at $"+str(auction_list.highest_bid.bidding)
        except Bid.DoesNotExist:
            winner = "This Listing is not active yet."

    # For Watchlist option
    if request.user.is_authenticated and auction_list.status==True:
        bid_option = True
        try:
            # Checks WatchList
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist = watchlist.listing_reference.get(pk=auction_list.id)
            watchlist_option = False
        except Auction_Listing.DoesNotExist:
            watchlist_option = True
    
    # For Bidding option
    if request.method == "POST":
        price = int(request.POST["price"])
        if price > auction_list.start_bid and (auction_list.highest_bid == None or price > auction_list.highest_bid.bidding):
            try:                
                bidder = Bid.objects.get(user=request.user,listing_reference=auction_list)
                bidder.bidding = price
                bidder.save()
            except Bid.DoesNotExist:
                bidder = Bid.objects.create(user=request.user,listing_reference=auction_list, bidding=price)
            
            auction_list.highest_bid = bidder
            auction_list.save()
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))
        else:
            error_message = "Please enter amount higher than current highest bid."
        
    # For Listing Comments
    if request.user.is_authenticated and auction_list.status==True:
        try:
            comment_option = Comment.objects.filter(listing_reference=auction_list)
        except Comment.DoesNotExist:
            pass

    return render(request, "auctions/listing.html",{
        "listing":auction_list,
        "watchlist":watchlist_option,
        "list_status":auction_list.status,
        "winner":winner,
        "bid_option":bid_option,
        "comments":comment_option,
        "error_message":error_message,
    })

@login_required(login_url='auctions:login')
def Add_to_Watchlist(request,listing_id):
    auction_list = Auction_Listing.objects.get(id=listing_id)
    if request.user.is_authenticated and auction_list.status==True:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
            watchlist.listing_reference.get(pk=auction_list.id)
            # If Listing_reference already exist(means user has clicked un-watch), so Delete WatchList
            watchlist.listing_reference.remove(auction_list)
        except Auction_Listing.DoesNotExist:
            # Add just listing_reference
            watchlist.listing_reference.add(auction_list)

    return HttpResponseRedirect(reverse("auctions:listing",args=(listing_id,)))

def Add_Comments(request,listing_id):
    if request.method == "POST":
        auction_list = Auction_Listing.objects.get(id=listing_id)
        comment = request.POST["comment"]
        Comment.objects.create(user=request.user, listing_reference=auction_list, comment=comment)

    return HttpResponseRedirect(reverse("auctions:listing",args=(listing_id,)))

def watchlist(request):
    all_listings = None
    try:
        my_watchlists = Watchlist.objects.get(user=request.user)
        all_listings = my_watchlists.listing_reference.all()
    except Watchlist.DoesNotExist:
        pass
    except Auction_Listing.DoesNotExist:
        pass
    return render(request, "auctions/watchlist.html",{
        "watchlists":all_listings
    })

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories":Category.objects.all()
    })

def category(request,category_id):
    try:
        category = Category.objects.get(pk=category_id)
        auction_list = Auction_Listing.objects.get(category=category)
    except Category.DoesNotExist:
        category = "No Categories Yet"
    except Auction_Listing.DoesNotExist:
        auction_list = "No Listing Yet"
    return render(request, "auctions/category.html",{
        "category":category,
        "auction_list":auction_list
    })

def close_listing(request,listing_id):
    auction_list = Auction_Listing.objects.get(pk=listing_id)
    auction_list.status = not (auction_list.status)
    auction_list.save()
    return HttpResponseRedirect(reverse("auctions:listing",args=(listing_id,)))