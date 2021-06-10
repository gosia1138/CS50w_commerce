from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('new/', views.create_view, name='new_listing'),
    path('details/<int:pk>/', views.detail_view, name='listing'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('bids/', views.users_bids_view, name='users_bids'),
    path('listings/', views.users_listings_view, name='users_listings'),
    path('search/', views.search_view, name='search'),
    path('category/<int:category>', views.category_view, name='category'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),


]
urlpatterns += staticfiles_urlpatterns()
