from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'hotel'

urlpatterns = [
    path("", hotel, name="hotel")
]
