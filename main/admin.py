from django.contrib import admin
from . import models
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, User, Cart, CartProduct, WishList, EnterProduct

# Oddiy modellarni ro'yxatdan o'tkazamiz
admin.site.register(User)
admin.site.register(models.CartProduct)
admin.site.register(models.WishList)
admin.site.register(models.EnterProduct)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'status_label', 'date', 'delivery_date', 'total_price', 'count_product')
    list_filter = ('status',)
    search_fields = ('code', 'user__username')
    actions = ('cancel_selected', 'delete_cancelled')

    @admin.display(description='Status')
    def status_label(self, obj):
        return obj.get_status_display()

    @admin.display(description='Jami narx')
    def total_price(self, obj):
        return obj.cart_total_price

    @admin.display(description='Mahsulotlar soni')
    def count_product(self, obj):
        return obj.count_product

    @admin.action(description="Bekor qilish (tanlanganlar)")
    def cancel_selected(self, request, queryset):
        count = 0
        for order in queryset.filter(status__in=(2, 3)):
            for item in order.cartproduct_set.all():
                if item.product:
                    item.product.count += item.count
                    item.product.save()
            order.status = 5
            order.delivery_date = None
            order.save()
            count += 1
        self.message_user(request, f"{count} ta buyurtma bekor qilindi.")

    @admin.action(description="O'chirish (bekor qilinganlar)")
    def delete_cancelled(self, request, queryset):
        cancelled = queryset.filter(status=5)
        count = cancelled.count()
        cancelled.delete()
        self.message_user(request, f"{count} ta bekor qilingan buyurtma o'chirildi.")

# Tarjima qilinadigan Category va Product modellarini TranslationAdmin orqali ro'yxatdan o'tkazamiz
@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'price', 'category')