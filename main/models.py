
from datetime import timedelta
from django.db import models
from django.utils import timezone
from uuid import uuid4

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=150, null= True, blank=True)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='users', null=True, blank=True)


    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"




class Code(models.Model):
    code = models.CharField(max_length=150, unique=True, default=uuid4, blank=True, null=True)


    def __str__(self):
        return self.code

    class Meta:
        abstract = True

class Category(models.Model):
    logo = models.ImageField(upload_to='categories')
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.name



class Product(Code):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

    @property
    def review_count(self):
        return self.reviews.count()



CART_STATUS = (
    (1, 'No Faol'),
    (2, "Yig'ilmoqda"),
    (3, "Yo'lda"),
    (4, "Yetkazilgan"),
    (5, "Bekor qilingan")
)

class Cart(Code):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CART_STATUS, default=1)
    date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)


    @property
    def cart_total_price(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += i.total_price
        return n


    @property
    def discount_total_price(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += i.discount_price
        return n

    @property
    def count_product(self):
        n = 0
        for i in CartProduct.objects.filter(cart=self):
            n += 1
        return n

    @property
    def estimated_delivery_date(self):
        """Yetkazib berish sanasi.

        - Buyurtma yetkazilgan bo'lsa, haqiqiy sana qaytadi.
        - Aks holda buyurtma sanasidan 3 kun keyingi sana olinadi.
        - Agar sana o'tib ketgan bo'lsa (eski buyurtma), avtomatik
          ravishda bugungi kunga moslab tuzatiladi.
        """
        if self.delivery_date:
            return self.delivery_date
        if self.status == 5:
            return None

        estimated = self.date + timedelta(days=3)
        now = timezone.now()
        if self.status in (2, 3) and timezone.localtime(estimated).date() < timezone.localdate():
            estimated = now + timedelta(days=1 if self.status == 3 else 2)
        return estimated

    def __str__(self):
        return f'{self.user} - {self.status}'


class CartProduct(Code):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()

    # Buyurtma berilgan paytdagi mahsulot ma'lumotlari (mahsulot o'chirilsa ham tarix saqlanadi)
    product_name = models.CharField(max_length=255, blank=True)
    product_image = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save_snapshot(self):
        """Mahsulotning hozirgi nomi, rasmi va narxini nusxalab qo'yadi."""
        product = self.product
        if not product:
            return
        self.product_name = product.name
        self.product_image = product.image.url if product.image else ''
        if product.status and product.discount_price:
            self.price = product.discount_price
            self.discount = product.price - product.discount_price
        else:
            self.price = product.price
            self.discount = 0

    @property
    def name(self):
        if self.product:
            return self.product.name
        return self.product_name or "Mahsulot o'chirilgan"

    @property
    def image(self):
        if self.product and self.product.image:
            return self.product.image.url
        return self.product_image or ''

    @property
    def unit_price(self):
        if self.product:
            if self.product.status and self.product.discount_price:
                return self.product.discount_price
            return self.product.price
        return self.price or 0

    @property
    def total_price(self):
        if self.product:
            if self.product.status and self.product.discount_price:
                return self.product.discount_price * self.count
            return self.product.price * self.count
        return (self.price or 0) * self.count

    @property
    def discount_price(self):
        if self.product:
            if self.product.status and self.product.discount_price:
                return (self.product.price - self.product.discount_price) * self.count
            return 0
        return (self.discount or 0) * self.count

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product}'
class EnterProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.count}'

    def save(self, *args, **kwargs):
        if self.pk:
            a = EnterProduct.objects.get(pk=self.pk)
            self.product.count = self.product.count - a.count
        self.product.count += self.count
        self.product.save()
        super().save(*args, **kwargs)

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product} - {self.rating}'