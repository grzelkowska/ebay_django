from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>", views.item, name="item"),
    path("<int:item_id>/add_to_watchlist", views.add_to_watchlist, name="watchlist"),
    path("<int:item_id>/bid", views.bid, name="bid"),
]
