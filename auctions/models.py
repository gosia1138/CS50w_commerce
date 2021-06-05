from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    def __str__(self):
        return '{}. {}'.format(self.pk, self.username)

    def bids(self):
        return self.bid_set.all()

    def listings(self):
        return self.listing_set.all()

class Listing(models.Model):
    # setting up list of categories
    categories = ['Electronics', 'Fashion', 'House & Garden', 'Beauty', 'Health',
        'Culture & Entertainment', 'Sport & Outdors', 'Moto', 'Art & Collectibles']
    CATS = []
    for i, category in enumerate(categories):
        CATS.append((i, category))
    CATS.append((99, 'Others'))
    # fields
    category = models.IntegerField(choices=CATS, default=99)
    title = models.CharField(max_length=120)
    image = models.URLField(blank=True)
    description = models.TextField()
    category = models.IntegerField(choices=CATS)
    time = models.DateTimeField(default=timezone.now)
    time_closed = models.DateTimeField(blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=30, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, related_name='watchlist', blank=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return '{}. "{}" - starting at {} €'.format(self.pk, self.title, self.starting_bid)

    def bids(self):
        return self.bid_set.all().order_by('-bid')

    def next_bid(self):
        if not self.bids():
            return float(self.starting_bid)
        else:
            return round(float(self.bids().first().bid) + 0.55)

    def close(self):
        self.closed = True
        self.time_closed = timezone.now()
        return Bid.objects.filter(listing=self.pk).order_by('-bid').first()

    def comments(self):
        return self.comment_set.all().order_by('-time')


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=30, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{} : {} - {}'.format(self.listing, self.user, self.bid)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    comment_content = models.TextField(verbose_name='Comment:')
