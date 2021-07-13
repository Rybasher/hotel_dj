from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'leisure'

urlpatterns = [
    path("", leisure, name="leisure")
]
