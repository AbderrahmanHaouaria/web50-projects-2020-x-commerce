from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.forms import widgets
from django.forms.widgets import HiddenInput, Input
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Comment, User, Listing, Bid
from django import forms

def index(request):
    return render(request, "auctions/index.html", {
        "listings": reversed(Listing.objects.all())
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
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

###############################################################################


def create(request):

    class ListingForm(forms.ModelForm):
        class Meta:
            model = Listing
            fields = ["title", "description", "starting_bid", "image", "category", "user"]
            widgets = {
                "user": HiddenInput,
            }

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("/")

    return render(request, "auctions/create.html", {
        "form": ListingForm(initial={"user": request.user})
    })


def listing(request, listingID):

    listing = Listing.objects.get(id=listingID)
    owner = listing.user
    visitor = request.user

    if listing.bid_set.last() is not None:
        highest_price = float(listing.bid_set.last().bid)
    else:
        highest_price = float(listing.starting_bid)

    class BidForm(forms.ModelForm):
        class Meta:
            model = Bid
            fields = ["bid", "listing", "user"]
            widgets = {
                "bid": Input(attrs={'type': 'number', 'min': f'{highest_price + 0.01}', 'class': 'form-control form-control-lg ps-3', 'placeholder': 'Bid', 'style': 'background-color: #CCD1E4; border-top-right-radius: 5px;'}),
                "listing": HiddenInput,
                "user": HiddenInput,
            }

    class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ["comment", "listing", "user"]
            widgets = {
                "comment": Input(attrs={'type': 'text', 'class': 'form-control form-control-lg ps-3', 'placeholder': 'Add a comment', 'autocomplete': 'off', 'style': 'background-color: #CCD1E4; border-bottom-right-radius: 5px;'}),
                "listing": HiddenInput,
                "user": HiddenInput,
            }

    if request.method == "POST" and visitor == owner:
        Listing.objects.filter(id=listingID).update(active=False)
        return HttpResponseRedirect(f"{listingID}")
    elif request.method == "POST" and "bid" in request.POST:
        form = BidForm(request.POST)
        if form.is_valid:
            form.save()
            highest_price = form.cleaned_data["bid"]
            return HttpResponseRedirect(f"{listingID}")
        else:
            return render(request, "auctions/listing.html", {
                "form": form
            })
    elif request.method == "POST" and "comment" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid:
            form.save()
        else:
            return HttpResponseRedirect(f"{listingID}")

    if visitor == owner:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(initial={"listing": listing, "user": visitor}),
        "comment": CommentForm(initial={"listing": listing, "user": visitor}),
        "highest_price": format(highest_price, ".2f"),
        "user_watchlist": visitor.watchlisted.all(),
        "owner": owner
        })
    elif visitor.is_authenticated:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(initial={"listing": listing, "user": visitor}),
        "comment": CommentForm(initial={"listing": listing, "user": visitor}),
        "highest_price": format(highest_price, ".2f"),
        "user_watchlist": visitor.watchlisted.all()
        })
    else:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": BidForm(initial={"listing": listing, "user": visitor}),
        "comment": CommentForm(initial={"listing": listing, "user": visitor}),
        "highest_price": format(highest_price, ".2f")
        })


def watchlist(request):
    if request.method == "POST":
        listingID = request.POST["listingID"]
        listing = Listing.objects.get(id=listingID)
        if listing in request.user.watchlisted.all():
            request.user.watchlisted.remove(listing)
            return HttpResponseRedirect(f"listing/{listingID}")
        else:
            request.user.watchlisted.add(listing)
            return HttpResponseRedirect(f"listing/{listingID}")
    return render(request, "auctions/watchlist.html", {
        "listings": request.user.watchlisted.all()
    })


def category(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category),
        "category": category
    })