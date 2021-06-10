from .models import Listing

def categories(request):
    return {
        'categories': Listing.Categories
}
