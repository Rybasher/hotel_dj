from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'offer'

urlpatterns = [
    path("", offer, name="offer")
]
