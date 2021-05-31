from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid


def index(request):
    context = {
        'listings': Listing.objects.all(),
    }
    return render(request, "auctions/index.html", context)


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        starting_bid = request.POST['starting_bid']
        user = request.user

        l = Listing(title=title, description=description, starting_bid=starting_bid, user=user)
        l.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/new.html')

def detail_view(request, pk):
    user = request.user
    listing = Listing.objects.get(pk=pk)
    bids = Listing.bids(listing)
    highest_bid = Listing.highest_bid(listing)
    if bids:
        your_bid = float(Listing.highest_bid(listing).bid) + 0.01
    else:
        your_bid = float(listing.starting_bid) + 0.01
    if request.method == 'POST':
        if 'watchlist' in request.POST:
            user.watchlist.add(listing)
        else:
            bid = request.POST['bid']
            user = request.user
            listing = Listing.objects.get(pk=pk)
            if float(bid) < float(highest_bid.bid):
                return render(request, 'auctions/listing.html', {
                    'pk': pk,
                    'listing':listing,
                    'bids': bids,
                    'highest_bid': highest_bid,
                    'your_bid': your_bid,
                    'message': 'Your bid must be higher than current highest bid!'
                })
            b = Bid(listing=listing, bid=bid, user=user)
            b.save()
        return HttpResponseRedirect(reverse('listing', args=[pk]))
    else:
        return render(request, 'auctions/listing.html', {
                'listing':listing,
                'bids': bids,
                'highest_bid': highest_bid,
                'your_bid': your_bid
            })


def watchlist_view(request):
    user = request.user

    if request.method == 'POST':
        for k, v in request.POST.items():
            if v == 'on':
                listing = Listing.objects.get(pk=k)
                user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse('watchlist'))
        # context = {
        #     'data': request.POST,
        #     }
        # return render(request, 'auctions/test.html', context)
    else:
        context = {
            'user': request.user,
        }
        return render(request, 'auctions/watchlist.html', context)
