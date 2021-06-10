from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

categories_list = ['Electronics', 'Fashion', 'House & Garden', 'Beauty', 'Health',
    'Culture & Entertainment', 'Sport & Outdors', 'Moto', 'Art & Collectibles']

class User(AbstractUser):
    def __str__(self):
        return '{}. {}'.format(self.pk, self.username)

    def bids(self):
        return self.bid_set.all()

    def listings(self):
        return self.listing_set.all()


class Listing(models.Model):
    # setting up list of categories
    class Categories(models.IntegerChoices):
        ELECTRONICS = 1, 'Electronics'
        FASHION = 2, 'Fashion'
        HOUSE = 3, 'House & Garden'
        BEAUTY = 4, 'Beauty'
        HEALTH = 5, 'Health'
        CULTURE = 6, 'Culture & Entertainment'
        SPORT = 7, 'Sport & Outdors'
        MOTO = 8, 'Moto'
        ART = 9, 'Art & Collectibles'
        OTHER = 99, ('Other')

        @classmethod
        def get_label(cls, id):
            for tup in cls.choices:
                if tup[0] == id:
                    return tup[1]



    # fields
    title = models.CharField(max_length=120)
    image = models.URLField(blank=True)
    description = models.TextField()
    category = models.IntegerField(choices=Categories.choices, blank=True)
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

    def n_watchers(self):
        return len(self.watchers.all())

    def n_bidders(self):
        bidders = [bid.user for bid in self.bid_set.all()]
        return len(set(bidders))


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
