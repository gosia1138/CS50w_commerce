from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from .forms import ListingForm, CommentForm, UserUpdateForm
from .models import User, Listing, Bid, Comment


def index(request):
    # List all active listings
    context = {
        'listings': Listing.objects.all().order_by('-time'),
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
                title=form.cleaned_data['title'],
                category=form.cleaned_data['category'],
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                starting_bid=form.cleaned_data['starting_bid'],
                user=request.user,
            )
            l.save()
            return HttpResponseRedirect(reverse('listing', args=[l.pk]))
    else:
        form = ListingForm()
        return render(request, 'auctions/new.html', {
            'form': form,
            'create':'create',
            })


def detail_view(request, pk):
    listing = Listing.objects.get(pk=pk)
    if request.method == 'POST':
        if 'close' in request.POST:
            listing.closed = True
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[pk]))
        # adding to watchlist
        if 'watchlist_add' in request.POST:
            request.user.watchlist.add(listing)
            return HttpResponseRedirect(reverse('listing', args=[pk]))
        if 'watchlist_remove' in request.POST:
            request.user.watchlist.remove(listing)
            return HttpResponseRedirect(reverse('listing', args=[pk]))
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
            else:
                return render(request, 'auctions/listing.html', {
                        'listing':listing,
                        'description': listing.description,
                        'watchers': len(listing.watchers.all()),
                        'bidders': set(bid.user for bid in Listing.bids(listing)),
                        'bids': Listing.bids(listing),
                        'next_bid': Listing.next_bid(listing),
                        'highest_bid': listing.bids().first(),
                        'comments': listing.comments(),
                        'comment_form': CommentForm(),
                        'bid_message': 'Miminum bid is {} €'.format(Listing.next_bid(listing))
                    })

        return HttpResponseRedirect(reverse('listing', args=[pk]))
    else:
        # Displaying the site (GET REQUEST)
        return render(request, 'auctions/listing.html', {
                'listing':listing,
                'description': listing.description,
                'watchers': len(listing.watchers.all()),
                'bidders': set(bid.user for bid in Listing.bids(listing)),
                'bidders_number': len(set(bid.user for bid in Listing.bids(listing))),
                'bids': Listing.bids(listing),
                'next_bid': Listing.next_bid(listing),
                'highest_bid': listing.bids().first(),
                'comments': listing.comments(),
                'comment_form': CommentForm()
            })

@login_required
def watchlist_view(request):
    if request.method == 'POST':
        for k, v in request.POST.items():
            if v == 'on':
                listing = Listing.objects.get(pk=k)
                request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse('watchlist'))
    else:
        context = {
            'listings': request.user.watchlist.all(),
            'watchlist': 'watchlist',
        }
        return render(request, 'auctions/watchlist.html', context)

@login_required
def users_bids_view(request):
    bids = request.user.bids()
    bids_l = set(bid.listing for bid in bids)
    context = {
        'listings': bids_l,
        'users_bids': 'users_bids',
    }
    return render(request, 'auctions/users_bids.html', context)

@login_required
def users_listings_view(request):
    listings = request.user.listings()
    context = {
        'listings': listings,
        'users_listings': 'users_listings',
    }
    return render(request, 'auctions/users_listings.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profile')
    else:
        return render(request, 'auctions/profile.html', {
            'form':UserUpdateForm(initial=model_to_dict(request.user)),
            'profile': 'profile',
        })

def search_view(request):
    if 'query' in request.GET:
        q = request.GET.get('query')
        cat = request.GET.get('category').lower()
        search_results = [entry for entry in Listing.objects.all() if q in entry.title.lower()]
        if cat != 'category':
            search_results = [entry for entry in search_results if entry.category == cat]

        return render(request, 'auctions/search.html', {
            'q': q,
            'listings': search_results,
        })
    else:
        return render(request, 'auctions/search.html', {
            'message': 'Type your query in the search field above.'
        })

def category_view(request, category):
    listings = Listing.objects.filter(category=category)
    cat_label = Listing.Categories.get_label(category)
    return render(request, 'auctions/category.html', {
        'listings': listings,
        'category': cat_label,
    })

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'auctions/change-password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)
