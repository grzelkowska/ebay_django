from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>", views.item, name="item"),
    path("<int:item_id>/add_to_watchlist", views.add_to_watchlist, name="add_watchlist"),
    path("<int:item_id>/bid", views.bid, name="bid"),
    path("<int:item_id>/close_bid", views.close_bid, name="close"),
    path("<int:item_id>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.category, name='category'),
    path("category/<int:category_id>", views.category_list, name="category_list"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("create_listing_new", views.create_listing_new, name="create_listing_new"),
    path("<int:comment_id>/delete_comment", views.delete_comment, name="delete_comment")
]
