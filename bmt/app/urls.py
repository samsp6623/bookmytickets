from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('locations/', Home.as_view(), name='home'),
    # path('performances/', Home.as_view(), name='home'),
    # path('shows/', Home.as_view(), name='home'),
    # path('booking/', Home.as_view(), name='home'),
    # path('login/', Home.as_view(), name='home'),
    # path('forgot-password/', Home.as_view(), name='home'),
    # path('dashboard/', Home.as_view(), name='home'),
    # path('profile/', Home.as_view(), name='home'),

    # path('locations/', Home.as_view(), name='home'),
    # path('locations/', Home.as_view(), name='home'),
    # path('locations/', Home.as_view(), name='home'),
    # path('locations/', Home.as_view(), name='home'),
]
