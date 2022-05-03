from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings


def index(request):
    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})


def item(request, item_id):
    try:
        listings = Listings.objects.get(id=item_id)
        user = request.user
    except:
        raise Http404("Item not found")

    return render(
        request,
        "auctions/item.html",
        {
            "id": listings.id,
            "title": listings.title,
            "description": listings.description,
            "starting_bid": listings.starting_bid,
            "current_bid": listings.current_bid,
            "category": listings.category,
            "active": listings.active,
            "created_date": listings.created_date,
            "creator": listings.creator,
            "watchers": listings.watchers.count(),
            "is_watched": listings.watchers.filter(pk=user.id)
            # "url": listings.url,
        },
    )


def add_to_watchlist(request, item_id):
    if request.method == "POST":
        item = Listings.objects.get(pk=item_id)
        user = request.user
        if item.watchers.filter(pk=user.id):
            item.watchers.remove(user.id)
        else:
            item.watchers.add(user.id)


    return HttpResponseRedirect(reverse("item", args=(item_id,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
