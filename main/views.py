import requests
from django.contrib import messages
from requests import Session
from requests.auth import HTTPBasicAuth
import geocoder
import calendar
from django.http import JsonResponse, HttpResponse
import datetime
from zeep import Client
from zeep.transports import Transport
import xml.etree.ElementTree as ET

from django.shortcuts import render, redirect
from django.views.generic import DetailView, View
from .models import *
from .forms import *
from hotel.settings import WSDL_CONFIG, EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError



# Create your views here.

session = Session()
session.auth = HTTPBasicAuth(WSDL_CONFIG["user"], WSDL_CONFIG["password"])
client = Client(WSDL_CONFIG["url"], transport=Transport(session=session))
service = client.service
factory = client.type_factory("ns0")


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


class AddReview(View):

    def post(self, request):
        print(request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['description']

            mail = send_mail(
                "Отзыв",
                f'От {name}, почта:{from_email} - отзыв: {message}',
                EMAIL_HOST_USER, ["kyrary99@gmail.com"], fail_silently=True
            )
            if mail:
                messages.success(request, 'письмо отправлено')
            else:
                messages.error(request, 'письмо не отправлено')
            form.save(commit=True)

        return redirect(request.META.get('HTTP_REFERER')
)


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


def get_rooms_xml(xml_data):
    root = ET.fromstring(xml_data)
    result = []
    for hotel_item in root:
        hotel = {
            "hotel": {
                "id": hotel_item.attrib['id'],
                "name": hotel_item.attrib["name"],
                "eci": hotel_item.attrib["eci"],
                "lco": hotel_item.attrib["lco"],
                "checkin": hotel_item.attrib["ckeckin"],
                "checkout": hotel_item.attrib["checkout"],
                "address": hotel_item.attrib["Adres"],
                "categories": []
            }

        }
        for category_item in hotel_item:
            if category_item.tag == "category":
                category = {
                    "id": category_item.attrib["id"],
                    "name": category_item.attrib["name"],
                    "rooms": []
                }
            for room_item in category_item:
                if room_item.tag == "room":
                    room = {
                        "number": room_item.attrib["num"],
                        "guests": room_item.attrib["addguests"],
                        "twin": False if room_item.attrib["twin"] == "false" else True,
                        "bathroom": room_item.attrib["bathroom"],
                        "level": room_item.attrib["level"]
                    }
                    category["rooms"].append(room)
            hotel["hotel"]["categories"].append(category)
        result.append(hotel)
    return result


def get_hotel_info(hotel):
    return {
        "name": hotel["name"],
        "id": hotel["id"],
        "address": hotel["address"],
        "eci": hotel["eci"],
        "lco": hotel["lco"],
        "checkin": hotel["checkin"],
        "checkout": hotel["checkout"]
    }


def get_apartaments_info(hotel):
    return [{"id": apartments_item["id"], "name": apartments_item["name"]} for apartments_item in hotel]


def get_all_rooms(hotel):
    rooms = []
    for apartment in hotel:
        for room_item in apartment["rooms"]:
            room = {
                "number": room_item["number"],
                "guests": room_item["guests"],
                "twin": room_item["twin"],
                "bathroom": room_item["bathroom"],
                "level": room_item["level"],
                "apartment_type": apartment["name"]
            }
            rooms.append(room)
    return rooms


class GetRooms(View):

    def get(self, request):
        location = request.GET.get("location_field", "")
        datn, datk = request.GET.get('datn', ''), request.GET.get('datk', '')
        datn = "".join(datn.split("-")) + "140000"
        datk = "".join(datk.split("-")) + "120000"

        persons = request.GET.get("persons_field", '')
        breakpoint()
        result = service.GetNomSvobod(datn, datk)
        result_json = get_rooms_xml(result)
        result_json = result_json[1] if location == "Ekaterina II" else result_json[1]
        hotel_info = get_hotel_info(result_json["hotel"])
        all_apartaments = get_apartaments_info(result_json["hotel"]["categories"])
        all_rooms = get_all_rooms(result_json["hotel"]["categories"])
        print(location, datn, datk, persons)
        # return redirect(request.META.get('HTTP_REFERER'))
        return render(request, "booking/booking.html", {"rooms": all_rooms})
