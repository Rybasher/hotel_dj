from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from hotel.settings import STATIC_ROOT, STATIC_URL

from django.urls import reverse
from django.utils import timezone
# Create your models here.
import datetime
from django.utils.html import format_html
from django.urls import reverse


_HOUR_RANGE = [(str(i), str(i)) for i in range(0, 24)]
_LEVELS = [(str(i), str(i)) for i in range(1, 6)]


class OrderStatus:
    CREATED = 0
    FAILED = 1
    SUCCESS = 2

    @classmethod
    def get_choices(cls):
        return [(str(i), str(i)) for i in range(0, 1)]


class Review(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголово отзыва", db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(verbose_name="Текст отзыва")
    image = models.ImageField(verbose_name="Фото отзыва")

    def __str__(self):
        return self.title


class Contact(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название контакта")
    slug = models.SlugField(max_length=255, unique=True)
    email = models.CharField(max_length=255, verbose_name="Почта контакта")
    number = models.CharField(max_length=30, verbose_name="Первый номер контакта")
    number_two = models.CharField(max_length=30, verbose_name="Второй номер контакта", null=True)

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"

    def __str__(self):
        return f"Контактные данные {self.title}"


class BookingContact(models.Model):

    title = models.CharField(max_length=255, verbose_name="Название контакта букинга")
    slug = models.SlugField(max_length=255, unique=True)
    email = models.CharField(max_length=255, verbose_name="Почта контакта")
    number = models.CharField(max_length=30, verbose_name="Первый номер контакта")
    number_two = models.CharField(max_length=30, verbose_name="Второй номер контакта", null=True)

    def __str__(self):
        return f"Контактные данные {self.title}"


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


def get_model_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class SightseeingItem(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Название экскурсии")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location)
    address = models.CharField(max_length=255, verbose_name="Адресс экскурсии")
    number = models.CharField(max_length=255, verbose_name="номер экскурсии")
    add_image = models.ImageField(upload_to=upload_location)


class SightseeingGuide(SightseeingItem):
    class Meta:
        verbose_name = "sightseeing_guide"
        verbose_name_plural = "sightseeing_guides"

    def __str__(self):
        return self.title


class SightseeingMuseum(SightseeingItem):
    class Meta:
        verbose_name = "sightseeing_museum"
        verbose_name_plural = "sightseeing_museums"

    def __str__(self):
        return self.title


class SightseeingNightGuide(SightseeingGuide):

    class Meta:
        verbose_name = "sightseeing_museum"
        verbose_name_plural = "sightseeing_museums"

    def __str__(self):
        return self.title


class SightseeingAddItem(models.Model):
    class Meta:
        verbose_name = "sightseeing_add_item"
        verbose_name_plural = "sightseeing_add_items"
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Название дополнительного элемента")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class GuideAddItem(SightseeingAddItem):
    sightseeing = models.ForeignKey(SightseeingGuide, blank=True, on_delete=models.CASCADE)


class NightGuideAddItem(SightseeingAddItem):
    sightseeing = models.ForeignKey(SightseeingNightGuide, blank=True, on_delete=models.CASCADE)


class MuseumAddItem(SightseeingItem):
    sightseeing = models.ForeignKey(SightseeingMuseum, blank=True, on_delete=models.CASCADE)


class SocialMedia(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название социальной сети")
    link = models.CharField(max_length=255, verbose_name="ссылка на социальную сеть")
    image = models.ImageField(verbose_name="Фото соц. сети")

    class Meta:
        verbose_name = "social_media"
        verbose_name_plural = "social_medias"

    def __str__(self):
        return self


class Offer(models.Model):
    title = models.CharField(max_length=255, verbose_name="название офера")
    image = models.ImageField(verbose_name="фото офера")
    details = models.TextField()

    class Meta:
        verbose_name = "offer"
        verbose_name_plural = "offers"

    def __str__(self):
        return self.title


class Video(models.Model):
    link = models.CharField(max_length=400, verbose_name="ссыллка на видео с ютуба")


class Hotel(models.Model):
    hotel_id = models.CharField(max_length=16, primary_key=True, unique=True)
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    early_check_in = models.CharField(max_length=2, choices=_HOUR_RANGE)
    late_check_out = models.CharField(max_length=2, choices=_HOUR_RANGE)
    check_in = models.CharField(max_length=2, choices=_HOUR_RANGE)
    check_out = models.CharField(max_length=2, choices=_HOUR_RANGE)
    address = models.CharField(max_length=32)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        verbose_name = "hotel"
        verbose_name_plural = "hotels"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hotel_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    category_id = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        unique_together = (('category_id', 'hotel_id'),)
        verbose_name = "category"
        verbose_name_plural = "categories"


class Room(models.Model):
    number = models.CharField(max_length=3)
    slug = models.SlugField(unique=True)
    guests = models.CharField(max_length=1)
    add_guests = models.CharField(max_length=1)
    twin = models.BooleanField()
    bathroom = models.CharField(max_length=32)
    level = models.IntegerField(choices=_LEVELS)
    option = models.CharField(max_length=32, null=True)
    category_id = models.CharField(max_length=16)
    hotel_id = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        unique_together = (('number', 'category_id', 'hotel_id'),)


class RoomImage(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    image = models.ImageField(null=False, upload_to=upload_location)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "room_image"
        verbose_name_plural = "room_images"

    def category_name(self):
        return self.category.name + " ( " + self.category.hotel_id.name + " )"

    def image_name(self):
        return self.image.name.replace(+"/", "")


class Text(models.Model):
    id = models.AutoField(primary_key=True)
    descriptor = models.CharField(max_length=64, unique=True)
    text_ru = models.TextField(null=True, blank=True)
    text_en = models.TextField(null=True, blank=True)
    text_ua = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "text"
        verbose_name_plural = "texts"
