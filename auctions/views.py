from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ListingForm, CommentForm
from .models import User, Listing, Bid, Comment


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
        form = ListingForm(request.POST)
        if form.is_valid():
            l = Listing(
                title = form.cleaned_data['title'],
                category = form.cleaned_data['category'],
                image = form.cleaned_data['image'],
                description = form.cleaned_data['description'],
                starting_bid = form.cleaned_data['starting_bid'],
                user = request.user,
            )
            l.save()
            return HttpResponseRedirect(reverse('listing', args=[l.pk]))
    else:
        form = ListingForm()
        return render(request, 'auctions/new.html', {'form':form})

def detail_view(request, pk):
    listing = Listing.objects.get(pk=pk)
    if request.method == 'POST':
        # DEBUGGING LINE:
        # keyword_test = 'watchlist' in request.POST
        # context = {
        #     'data': request.POST,
        #     'keyword_test': keyword_test,
        # }
        # return render(request, 'auctions/debug.html', context)

        if 'close' in request.POST:
            listing.closed = True
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[pk]))
        # adding to watchlist
        if 'watchlist' in request.POST:
            request.user.watchlist.add(listing)
        # comments section
        if 'comment_content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                c = Comment(
                    user = request.user,
                    listing = listing,
                    comment_content = comment_form.cleaned_data['comment_content']
                )
                c.save()
                return HttpResponseRedirect(reverse('listing', args=[pk]))
        # bidding
        else:
            bid = float(request.POST.get('bid', 0))
            if bid >= listing.next_bid():
                b = Bid(user=request.user, listing=listing, bid=bid)
                b.save()
        return HttpResponseRedirect(reverse('listing', args=[pk]))
    else:
        return render(request, 'auctions/listing.html', {
                'listing':listing,
                'watchers': len(listing.watchers.all()),
                'bids': Listing.bids(listing),
                'next_bid': Listing.next_bid(listing),
                'highest_bid': listing.bids().first(),
                'comments': listing.comments(),
                'comment_form': CommentForm()
            })


def watchlist_view(request):
    if request.method == 'POST':
        for k, v in request.POST.items():
            if v == 'on':
                listing = Listing.objects.get(pk=k)
                request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse('watchlist'))
    else:
        return render(request, 'auctions/watchlist.html')
