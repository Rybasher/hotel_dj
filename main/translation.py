from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name', 'address')


