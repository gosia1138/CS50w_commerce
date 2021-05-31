from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('new/', views.create_view, name='new_listing'),
    path('<int:pk>/', views.detail_view, name='listing'),

]
