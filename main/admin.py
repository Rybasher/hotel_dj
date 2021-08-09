from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *
# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'number', 'number_two']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SightseeingGuide)
class SightseeingGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'address', 'number', 'add_image']


@admin.register(SightseeingMuseum)
class SightseeingMuseumAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'address', 'number', 'add_image']


@admin.register(SightseeingNightGuide)
class SightseeingNightGuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'address', 'number', 'add_image']


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'image']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['hotel_id', 'name', 'address']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hotel_id', 'category_id', 'number']
    prepopulated_fields = {'slug': ('number',)}



admin.site.register(RoomImage)



