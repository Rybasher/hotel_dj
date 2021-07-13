from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'contacts'

urlpatterns = [
    path("", contacts, name="contacts")
]
