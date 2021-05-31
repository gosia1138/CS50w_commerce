from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass
    def __str__(self):
        return '{}. {}'.format(self.pk, self.username)


class Listing(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=30, decimal_places=2)
    # current_bid = models.DecimalField(max_digits=30, decimal_places=2, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, related_name='watchlist')

    def __str__(self):
        return '{}. "{}" - starting at {} €'.format(self.pk, self.title, self.starting_bid)

    def bids(self):
        return Bid.objects.filter(listing=self.pk).order_by('-bid')

    def highest_bid(self):
        return Bid.objects.filter(listing=self.pk).order_by('-bid').first()


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return '{} : {} - {}'.format(self.listing, self.user, self.bid)


class Comment(models.Model):
    pass
