import requests
import base64
import os
import subprocess
from django.contrib import messages
from requests import Session
from requests.auth import HTTPBasicAuth
import geocoder
import tempfile

import calendar
from django.http import JsonResponse, HttpResponse
import datetime
from zeep import Client
from zeep.transports import Transport
from zeep.helpers import *
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.views.generic import DetailView, View
from .models import *
from .forms import *
from hotel.settings import WSDL_CONFIG, EMAIL_HOST_USER, UPC_CONFIG, BASE_DIR
from django.core.mail import send_mail, BadHeaderError
from .validate import *
import json


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


class HoteDeailView(View):
    def get(self, request, slug):
        hotel = Hotel.objects.get(slug__iexact=slug)
        return render(request, 'hotel/hotel.html', {"hotel": hotel})


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
        hotels = Hotel.objects.all()

        return render(request, 'leisure/leisure.html', {})


class SpecialOfferView(View):
    def get(self, request, *args, **kwargs):
        hotels = Hotel.objects.all()

        return render(request, 'offer/offer.html', {})


class Booking(View):
    def get(self, request, *args, **kwargs):
        hotels = Hotel.objects.all()
        return render(request, 'booking/booking.html', {'hotels': hotels})


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
                    "hotel_id": hotel_item.attrib["id"],
                    "tariffs": [],
                    "rooms": []
                }
            for tarif_item in category_item:
                if tarif_item.tag == "tarif":
                    tarif = {
                        "id": tarif_item.attrib["id"],
                        "name": tarif_item.attrib["name"],
                        "name_eng": tarif_item.attrib["nameENG"],
                        "description": tarif_item.attrib["description"],
                        "eciprice": tarif_item.attrib["eciprice"],
                        "lcoprice": tarif_item.attrib["lcoprice"],
                        "address": tarif_item.attrib["Adres"],

                        'price': {}
                    }
                    for price_item in tarif_item:
                        if price_item.tag == "price":
                            price = {
                                "daten": price_item.attrib["dateN"],
                                "datek": price_item.attrib["dateK"],
                                "roomprice": price_item.attrib["roomprice"],
                                "twinprice": price_item.attrib["twinprice"],
                                "bkfprice": price_item.attrib["bkfprice"],
                                "kvodop": price_item.attrib["KvoDop"]
                            }
                            tarif["price"].update(price)
                    category["tariffs"].append(tarif)
            for room_item in category_item:
                if room_item.tag == "room":
                    room = {
                        "category_id": category_item.attrib["id"],
                        "number": room_item.attrib["num"],
                        "guests": room_item.attrib["addguests"],
                        "twin": False if room_item.attrib["twin"] == "false" else True,
                        "bathroom": room_item.attrib["bathroom"],
                        "level": room_item.attrib["level"],
                        "option": []
                    }
                    for option_item in room_item:
                        option = {
                            "option": option_item.text if hasattr(option_item, 'text') else ""
                        }
                        room["option"].append(option)
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


def get_free_rooms(categories):
    return categories


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
        hotels = Hotel.objects.all()
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        location = request.GET.get("location_field", "")
        checkin, checkout = request.GET.get("checkin_field", "140000"), request.GET.get("checkout_checkout", "120000")
        datn, datk = request.GET.get('datn', ''), request.GET.get('datk', '')
        # try:
        # except:
        #     print("no checkin and checkout")
        daten_cart, datek_cart = datn, datk
        breakpoint()
        # daten_name, datek_name =
        datn = "".join(datn.split("-")) + "140000"
        datk = "".join(datk.split("-")) + "120000"
        # if checkin and checkout:
        #     checkin = "".join(checkin.split(":")) + "00"
        #     checkout = "".join(checkout.split(":")) + "00"
        #     if len(checkin.split()) == 5:
        #         checkin = "0" + checkin
        #     if len(checkout.split()) == 5:
        #         checkout = "0" + checkout
        # else:
        #     checkin = "140000"
        #     checkout = "120000"
        # datn += checkin
        # datk += checkout
        persons = request.GET.get("persons_field", '')
        result = service.GetNomSvobod(datn, datk)
        result_json = get_rooms_xml(result)
        result_json = result_json[0] if location == "Ekaterina II" else result_json[1]
        hotel_info = get_hotel_info(result_json["hotel"])
        all_free_rooms = get_free_rooms(result_json["hotel"]["categories"])
        print(location, datn, datk, persons)
        context = {
            "rooms": all_free_rooms,
            "hotels": hotels,
            "datn": datn,
            "datk": datk,
            "checkin": checkin,
            "checkout": checkout
        }
        return render(request, "booking/booking.html", context)


class BlockCategory(View):

    def post(self, request):
        post_data = json.loads(request.body.decode("utf-8"))
        valid_data = validate_block_category(post_data)
        number = factory.spiszakaz(factory.zakaz(
            valid_data["hotel_id"],
            valid_data["category_id"],
            valid_data["tariff_id"],
            "1",
            "0",
            "false",
            "false",
            "1",
        ))
        block_category = service.BlockCategory(
            valid_data["datn"],
            valid_data["datk"],
            "20",
            number,
            valid_data["tariff_price"]
        )
        block_category_result = serialize_object(block_category)
        result = {
            "hotel_id": valid_data["hotel_id"],
            "category_id": valid_data["category_id"],
            "tariff_id": valid_data["tariff_id"],
            "category_name": valid_data["category_name"],
            "tariff_name": valid_data["tariff_name"],
            "tariff_price": valid_data["tariff_price"],
            "idzakaza": block_category_result["idzakaza"]
        }

        return JsonResponse({"data": result})


class BlockCancel(View):
    def post(self, request):
        post_data = json.loads(request.body.decode("utf-8"))
        result = service.BlockCancel(post_data)
        return JsonResponse({"data": serialize_object(result)})


class BlockContinue(View):
    def post(self, request):
        post_data = json.loads(request.body.decode("utf-8"))

        valid_data = validate_block_continue(post_data)
        result = service.BlockCancel(valid_data)
        return JsonResponse({"data": serialize_object(result)})


class BlockPay(View):
    def post(self, request):
        try:
            post_data = json.loads(request.body.decode("utf-8"))

            valid_data = valid_order_data(post_data)

            data_to_store = {
                "idzakaza": valid_data["datatostore"][0]["idzakaza"],
                "datn": "2021-10-18",
                "datk": "2021-10-19",
                "timen": "14:00",
                "timeek": "12:00",
                "hotel_id": valid_data["datatostore"][0]["hotel_id"],
                "category_id": valid_data["datatostore"][0]["category_id"],
                "guests": 1,
                "addguests": 0,
                "breakfast": 0,
                "tariff_id": valid_data["datatostore"][0]["tariff_id"],
                "twin": 0,
                "costdesc": "(2021-10-18+12:00+-+2021-10-19+12:00)+1+x+1+UAH",
                "cost": "1",
                "surname": valid_data["l_name"],
                "firstname": valid_data["name"],
                "secondname": "Sec Name",
                "phone": valid_data["phone"],
                "email": valid_data["email"],
                "order_type": 1,
                "paid": 0
            }
            spisid = factory.spisid([factory.idblock(_id) for _id in valid_data["spisid"]])
            fio = factory.FIO(
                valid_data["l_name"],
                valid_data["name"],
                "Леонтьев",
                valid_data["phone"],
                valid_data["email"])
            id_zak = service.BlockPay(spisid, fio)
            result = {
                "totalAmount": 1101,
                "locale": "ru",
                "orderid": id_zak["id"],
                "fio": {
                    "surname": valid_data["l_name"],
                    "name": valid_data["name"],
                    "second_name": "leontiev",
                    "phone": valid_data["phone"],
                    "email": valid_data["email"]
                }
            }
            breakpoint()
            return JsonResponse({"data": serialize_object(result)})
        except Exception as e:
            print("error" + e)
            return JsonResponse({"message": str(e)})


class UpcPay(View):
    def post(self, request):
        try:
            post_data = json.loads(request.body.decode("utf-8"))
            valid_data = valid_order_data(post_data)
            breakpoint()
            personal_data = valid_data["fio"]
            email = personal_data["email"]

            personal_data = personal_data["surname"] + " " + personal_data["name"] + " " + personal_data["second_name"]
            breakpoint()
            version = UPC_CONFIG["version"]
            merchant_id = UPC_CONFIG["merchantId"]
            terminal_id = UPC_CONFIG["terminalId"]
            total_amount = str(int(100 * valid_data["totalAmount"]))
            breakpoint()
            currency = UPC_CONFIG["currency"]
            purchase_time = datetime.datetime.now().strftime(UPC_CONFIG["dateFormat"])
            locale = valid_data["locale"]
            order_id = valid_data["orderid"]
            breakpoint()

            sd = {
                "locale": valid_data["locale"],
                "personalData": valid_data["fio"],
                "paymentType": "paid",
                "sendEmail": True if email else False
            }
            breakpoint()
            sd = base64.b64encode(json.dumps(sd).encode('utf-8')).decode('utf-8')
            breakpoint()
            data_file_content = f"{merchant_id};{terminal_id};{purchase_time};{order_id};{currency};{total_amount};{sd};"
            data_file, data_file_name = tempfile.mkstemp()
            data_file = open(data_file_name, "w")
            data_file.write(data_file_content)
            data_file.close()
            breakpoint()
            # private_key = open(os.path.join(BASE_DIR, UPC_CONFIG["privateKey"]), "r")
            # print(f"data_file_content {data_file_content}")
            # print(f"data_file_name {data_file_name}")
            # command1 = f"openssl dgst -sha1 -sign {private_key.name} {data_file_name} | openssl base64 -e"
            # print(command1)
            breakpoint()
            # p1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
            # signature = p1.communicate()[0].decode('latin1')
            # print(f"signature {signature}")
            # private_key.close()
            # os.remove(data_file_name)
            breakpoint()
            post_fields = {
                "Version": version,
                "MerchantID": merchant_id,
                "TerminalID": terminal_id,
                "TotalAmount": total_amount,
                "Currency": currency,
                "PurchaseTime": purchase_time,
                "locale": locale,
                "OrderID": str(order_id),
                "PurchaseDesc": personal_data,
                # "Signature": signature,
                "SD": sd
            }
            return JsonResponse({"data": serialize_object(post_fields)})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "ERROR", "message": str(e)})



