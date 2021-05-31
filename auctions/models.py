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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '"{}" - starting at {} €'.format(self.title, self.starting_bid)
