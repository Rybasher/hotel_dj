from django.urls import path
from .views import *

urlpatterns = [
    path("", BaseView.as_view(), name="home_page"),
    path("search_room", GetRooms.as_view(), name="get_rooms"),
    path("contacts", ContactsView.as_view(), name="contacts"),
    path("review", AddReview.as_view(), name="add_review"),
    path("sightseeing", SightseeingView.as_view(), name="sightseeing"),
    path("offer", SpecialOfferView.as_view(), name="special_offer"),
    path("hotel", HotelPageView.as_view(), name="hotel"),
    path("booking", Booking.as_view(), name="booking"),

]