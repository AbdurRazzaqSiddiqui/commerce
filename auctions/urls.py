from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/comments", views.Add_Comments, name="add_comment"),
    path("listing/close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("watchlist/<int:listing_id>", views.Add_to_Watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="my_watchlist"),
    path("categories", views.categories, name="all_categories"),
    path("categories/<int:category_id>", views.category, name="category"),
]
