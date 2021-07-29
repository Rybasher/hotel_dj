import requests
from requests import Session
from requests.auth import HTTPBasicAuth
import geocoder
import calendar
import datetime
from zeep import Client
from zeep.transports import Transport
import xml.etree.ElementTree as ET

from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import *
from hotel.settings import WSDL_CONFIG



# Create your views here.

# session = Session()
# session.auth = HTTPBasicAuth(WSDL_CONFIG["user"], WSDL_CONFIG["password"])
# client = Client(WSDL_CONFIG["url"], transport=Transport(session=session))
# service = client.service
# factory = client.type_factory("ns0")


class Geoposition:

    @staticmethod
    def get_geo():
        geoposition  = geocoder.ip("me")
        return {'country': geoposition.country,
                'city': geoposition.city
                }

    @staticmethod
    def get_weather(city, api):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                               params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': api})
            return res
        except Exception as e:
            raise Exception("Exception (forecast):", e)

    @staticmethod
    def get_date():
        date = datetime.datetime.now()
        month = calendar.month_name[datetime.datetime.today().month]
        return {
            'year': date.year,
            'month_id': date.month,
            'day_id': date.day,
            'hour': date.hour,
            'minutes': date.minute,
            'month_name': month
        }


class BaseView(View):
    API = "6a19ae9f912647a29273aef51735012d"

    def get(self, request, *args, **kwargs):
        geoposition = Geoposition.get_geo()
        weather = Geoposition.get_weather(geoposition["city"], self.API).json()
        date = Geoposition.get_date()
        reviews = Review.objects.all()
        hotels = Hotel.objects.all()
        rooms = Hotel.objects.all()
        context = {
            'year': date["year"],
            'month_name': date["month_name"],
            'day_id': date["day_id"],
            'hours': date["hour"],
            'minutes': date["minutes"],
            'weather_desc': weather["weather"][0]["description"],
            'weather_temp': weather["main"]["temp"],
            'reviews': reviews,
            'hotels': hotels,
            'rooms': rooms
        }
        return render(request, 'home/home.html', context)


class ContactsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'contacts/contacts.html', {})


class SightseeingView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'leisure/leisure.html', {})


class SpecialOfferView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'offer/offer.html', {})


class HotelPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hotel/hotel.html')


class Booking(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'booking/booking.html')