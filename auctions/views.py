from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listings, Bids, Comments, Categories


def index(request):
    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})


def item(request, item_id):
    is_watched = False
    is_creator = False
    is_buyer = False
    listings = Listings.objects.get(id=item_id)
    comments = Comments.objects.filter(listing=listings)
    categories = Categories.objects.get(category=listings.category)
    if request.user.id:
        user = request.user
        creator = User.objects.get(username=user.username)

        if creator == listings.creator:
            is_creator = True
        is_buyer = False
        if user == listings.buyer:
            is_buyer = True
        is_watched = listings.watchers.filter(pk=user.id)

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
            "is_watched": is_watched,
            "is_creator": is_creator,
            "is_buyer": is_buyer,
            "useruser": request.user,
            "comments": comments,
            "category_id": categories.id,
            "image": listings.image,
        },
    )


def create_listing(request):

    return render(request, "auctions/create_listing.html")


def create_listing_new(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = float(request.POST["starting_bid"])
        category = request.POST["category"]
        if Categories.objects.filter(category=category):
            create_category = Categories.objects.get(category=category)
        else:
            create_category = Categories(category=category)
            create_category.save()
        creator = request.user
        image = request.FILES.get("image")
        new_posting = Listings(
            title=title,
            description=description,
            starting_bid=starting_bid,
            creator=creator,
            category=create_category,
            image=image,
        )
        new_posting.save()

    return render(request, "auctions/index.html", {"listings": Listings.objects.all()})


def category(request):
    categories = Categories.objects.all()

    return render(
        request,
        "auctions/category.html",
        {
            "categories": categories,
        },
    )


def category_list(request, category_id):
    categories = Listings.objects.filter(category=category_id)

    return render(
        request,
        "auctions/categoryList.html",
        {
            "categories": categories,
        },
    )


@login_required
def watchlist(request):
    watchlists = request.user.watch_list.all()

    return render(request, "auctions/watchlist.html", {"watchlists": watchlists})


@login_required
def add_to_watchlist(request, item_id):
    if request.method == "POST":
        item = Listings.objects.get(pk=item_id)
        user = request.user
        if item.watchers.filter(pk=user.id):
            item.watchers.remove(user.id)
        else:
            item.watchers.add(user.id)
    return HttpResponseRedirect(reverse("item", args=(item_id,)))


@login_required
def comment(request, item_id):
    if request.method == "POST":
        item = Listings.objects.get(pk=item_id)
        user = request.user
        your_comment = request.POST["your_comment"]
        newComment = Comments(user=user, listing=item, comment=your_comment)
        newComment.save()
    return HttpResponseRedirect(reverse("item", args=(item_id,)))


@login_required
def delete_comment(request, comment_id):
    if request.method == "POST":
        your_comment = Comments.objects.get(id=comment_id)
        if your_comment.user == request.user:
            your_comment.delete()
    return HttpResponseRedirect(reverse("item", args=(your_comment.listing.id,)))


@login_required
def bid(request, item_id):
    if request.method == "POST":
        item = Listings.objects.get(pk=item_id)
        username = request.user.username
        user = User.objects.get(username=username)
        your_bid = float(request.POST["your_bid"])
        if item.current_bid:
            bid_price = item.current_bid
        else:
            bid_price = item.starting_bid

        if float(request.POST["your_bid"]) <= bid_price:
            messages.warning(
                request, "Your bid must be higher than the current bid price."
            )

        else:
            item.current_bid = your_bid
            item.save()
            newBid = Bids.objects.filter(auction=item)
            if newBid:
                newBid.delete()
            newBid = Bids(auction=item, offer=your_bid, user=user)
            newBid.save()

    return HttpResponseRedirect(reverse("item", args=(item_id,)))


@login_required
def close_bid(request, item_id):
    if request.method == "POST":
        item = Listings.objects.get(pk=item_id)
        item.active = False
        item.save()

        bid = Bids.objects.get(auction=item)
        user = bid.user
        item.buyer = user
        item.save()

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
