from django.forms import ModelForm
from .models import Bid, Comment, Listing


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
