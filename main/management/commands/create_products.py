from django.core.management.base import BaseCommand
from main.models import Category, Product

class Command(BaseCommand):
    help = 'Mahsulotlarni nomiga mos rasmlar bilan yaratish'

    def handle(self, *args, **kwargs):
        self.stdout.write("Eski ma'lumotlar tozalanmoqda...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Kategoriyalar
        cat_elec = Category.objects.create(name_uz="Elektronika", name_ru="Электроника", name_en="Electronics")
        cat_clothes = Category.objects.create(name_uz="Kiyim-kechak", name_ru="Одежда", name_en="Clothing")
        cat_home = Category.objects.create(name_uz="Uy jihozlari", name_ru="Для дома", name_en="Home Appliances")
        cat_books = Category.objects.create(name_uz="Kitoblar", name_ru="Книги", name_en="Books")
        cat_sports = Category.objects.create(name_uz="Sport buyumlari", name_ru="Спорттовары", name_en="Sports Goods")

        # Har bir mahsulotga mos unikal rasm (Unsplash orqali yoki mavjud statik rasmlar)
        products_data = [
            {
                "name_uz": "Smartfon X12", "name_ru": "Смартфон X12", "name_en": "Smartphone X12",
                "desc_uz": "Zamonaviy va kuchli smartfon.", "desc_ru": "Современный и мощный смартфон.", "desc_en": "Modern smartphone.",
                "price": 3500000, "disc": 3200000, "count": 15, "code": "el-01", "cat": cat_elec,
                "img": "thumbs/tech-icon1.png"
            },
            {
                "name_uz": "Noutbuk Pro 15", "name_ru": "Ноутбук Pro 15", "name_en": "Laptop Pro 15",
                "desc_uz": "Tezkor noutbuk.", "desc_ru": "Быстрый ноутбук.", "desc_en": "Fast laptop.",
                "price": 7500000, "disc": 7100000, "count": 10, "code": "el-02", "cat": cat_elec,
                "img": "thumbs/tech-icon2.png"
            },
            {
                "name_uz": "Simsiz Quloqchin", "name_ru": "Наушники", "name_en": "Wireless Earbuds",
                "desc_uz": "Toza ovoz.", "desc_ru": "Чистый звук.", "desc_en": "Clean sound.",
                "price": 450000, "disc": 399000, "count": 40, "code": "el-03", "cat": cat_elec,
                "img": "thumbs/tech-icon3.png"
            },
            {
                "name_uz": "Smart Soat T8", "name_ru": "Смарт-часы", "name_en": "Smart Watch",
                "desc_uz": "Salomatlik uchun.", "desc_ru": "Для здоровья.", "desc_en": "Health tracker.",
                "price": 600000, "disc": 550000, "count": 25, "code": "el-04", "cat": cat_elec,
                "img": "thumbs/tech-icon4.png"
            },
            {
                "name_uz": "Erkaklar Ko'ylagi", "name_ru": "Мужская рубашка", "name_en": "Men's Shirt",
                "desc_uz": "Paxtali ko'ylak.", "desc_ru": "Хлопковая рубашка.", "desc_en": "Cotton shirt.",
                "price": 180000, "disc": 150000, "count": 30, "code": "cl-01", "cat": cat_clothes,
                "img": "thumbs/tech-icon5.png"
            },
            {
                "name_uz": "Sport Kostyumi", "name_ru": "Спортивный костюм", "name_en": "Sport Suit",
                "desc_uz": "Sport uchun.", "desc_ru": "Для спорта.", "desc_en": "Sportswear.",
                "price": 450000, "disc": 400000, "count": 20, "code": "cl-02", "cat": cat_clothes,
                "img": "thumbs/tech-icon6.png"
            },
            {
                "name_uz": "Qozon To'plami", "name_ru": "Набор казанов", "name_en": "Cauldron Set",
                "desc_uz": "Sifatli qozonlar.", "desc_ru": "Качественные казаны.", "desc_en": "Quality cauldrons.",
                "price": 500000, "disc": 450000, "count": 18, "code": "hm-01", "cat": cat_home,
                "img": "thumbs/tech-icon7.png"
            },
            {
                "name_uz": "Python Asoslari", "name_ru": "Основы Python", "name_en": "Python Basics",
                "desc_uz": "Kitob.", "desc_ru": "Книга.", "desc_en": "Book.",
                "price": 80000, "disc": 70000, "count": 40, "code": "bk-01", "cat": cat_books,
                "img": "thumbs/tech-icon8.png"
            },
            {
                "name_uz": "Futbol To'pi", "name_ru": "Футбольный мяч", "name_en": "Football",
                "desc_uz": "O'yin uchun.", "desc_ru": "Для игры.", "desc_en": "For game.",
                "price": 220000, "disc": 190000, "count": 28, "code": "sp-01", "cat": cat_sports,
                "img": "thumbs/tech-icon9.png"
            },
        ]

        for item in products_data:
            p = Product.objects.create(
                name_uz=item["name_uz"],
                name_ru=item["name_ru"],
                name_en=item["name_en"],
                description_uz=item["desc_uz"],
                description_ru=item["desc_ru"],
                description_en=item["desc_en"],
                price=item["price"],
                discount_price=item["disc"],
                count=item["count"],
                code=item["code"],
                category=item["cat"]
            )
            # Rasm yo'lini to'g'ridan-to'g'ri biriktiramiz
            p.image = item["img"]
            p.save()

        self.stdout.write(self.style.SUCCESS("Mahsulotlar o'z rasmlari bilan yaratildi!"))