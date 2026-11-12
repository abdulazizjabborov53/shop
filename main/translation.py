from modeltranslation.translator import translator, TranslationOptions
from .models import Product, Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Kategoriyaning tarjima qilinadigan maydonlari

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')  # Mahsulotning tarjima qilinadigan maydonlari

translator.register(Category, CategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)