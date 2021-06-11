
from django import forms
from django.forms import ModelForm
from .models import Bid, Comment, Listing, User, Profile


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'image', 'description', 'starting_bid']


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_content']


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
