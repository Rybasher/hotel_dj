from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'booking'

urlpatterns = [
    path("", booking, name="booking")
]
