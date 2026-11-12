from django.core.management.base import BaseCommand
from main.models import Category, Product
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Generate sample categories and products'

    def handle(self, *args, **options):
        # Sample categories (50+)
        categories_data = [
            "Elektronika", "Telefonlar", "Kompyuterlar", "Noutbuklar", "Planshetlar",
            "Televizorlar", "Audio texnika", "Kameralar", "O'yin konsollari", "Aksessuarlar",
            "Kiyimlar", "Erkaklar kiyimi", "Ayollar kiyimi", "Bolalar kiyimi", "Poyabzallar",
            "Sumkalar", "Soatlar", "Zargarlik buyumlari", "Kosmetika", "Parfyumeriya",
            "Uy-ro'zg'or", "Mebel", "Kuchma jihozlar", "Oshxona jihozlari", "Idish-tovoqlar",
            "To'qimachilik", "Choyshablar", "Yostiqchalar", "Pardalar", "Gilamlar",
            "Sport", "Fitnes jihozlari", "Velosipedlar", "Futbol", "Basketbol", "Tennis",
            "Kitoblar", "Badiiy adabiyot", "Ilmiy adabiyot", "Dasturlash", "Bolalar kitoblari",
            "Oziq-ovqat", "Mevalar", "Sabzavotlar", "Sut mahsulotlari", "Non mahsulotlari",
            "Ichimliklar", "Shirinliklar", "Qahva", "Choy", "Sharbatlar",
            "Avto", "Ehtiyot qismlar", "Aksessuarlar", "Moylar", "Shinalar",
            "Qurilish", "Qurilish materiallari", "Elektr jihozlari", "Instrumentlar", "Sanitexnika"
        ]

        self.stdout.write('Generating categories...')
        for cat_name in categories_data:
            Category.objects.get_or_create(
                name=cat_name,
                defaults={'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories_data)} categories'))

        # Sample products (50+)
        products_data = [
            ("iPhone 15 Pro Max", 15000000, 13500000, "Elektronika"),
            ("Samsung Galaxy S24", 12000000, 11000000, "Elektronika"),
            ("MacBook Pro 14", 25000000, 23000000, "Kompyuterlar"),
            ("Dell XPS 15", 18000000, 16500000, "Kompyuterlar"),
            ("iPad Pro 12.9", 10000000, 9000000, "Planshetlar"),
            ("Samsung Galaxy Tab", 6000000, 5500000, "Planshetlar"),
            ("Sony Bravia 65\"", 8000000, 7200000, "Televizorlar"),
            ("LG OLED 55\"", 12000000, 10800000, "Televizorlar"),
            ("Bose SoundLink", 2000000, 1800000, "Audio texnika"),
            ("Sony WH-1000XM5", 3500000, 3200000, "Audio texnika"),
            ("Canon EOS R5", 15000000, 13500000, "Kameralar"),
            ("Sony A7 IV", 13000000, 12000000, "Kameralar"),
            ("PlayStation 5", 7000000, 6500000, "O'yin konsollari"),
            ("Xbox Series X", 6500000, 6000000, "O'yin konsollari"),
            ("Nike Air Max", 1500000, 1200000, "Poyabzallar"),
            ("Adidas Ultraboost", 1800000, 1500000, "Poyabzallar"),
            ("Levi's Jeans", 800000, 700000, "Erkaklar kiyimi"),
            ("Zara Kofta", 500000, 400000, "Ayollar kiyimi"),
            ("H&M Bolalar kiyimi", 300000, 250000, "Bolalar kiyimi"),
            ("Michael Kors Sumka", 2500000, 2000000, "Sumkalar"),
            ("Rolex Submariner", 50000000, 45000000, "Soatlar"),
            ("Omega Seamaster", 35000000, 32000000, "Soatlar"),
            ("Dior Parfyumeriya", 3000000, 2700000, "Parfyumeriya"),
            ("Chanel No. 5", 4000000, 3500000, "Parfyumeriya"),
            ("IKEA Divan", 5000000, 4500000, "Mebel"),
            ("Drezina Stol", 2000000, 1800000, "Mebel"),
            ("Samsung Kirish mashinasi", 4000000, 3600000, "Kuchma jihozlar"),
            ("LG Sovutgich", 6000000, 5400000, "Kuchma jihozlar"),
            ("Philips Blender", 800000, 700000, "Oshxona jihozlari"),
            ("Tefal Tovagich", 500000, 450000, "Oshxona jihozlari"),
            ("Nike Fitnes to'plami", 1000000, 800000, "Sport"),
            ("Adidas Fitnes to'plami", 900000, 750000, "Sport"),
            ("Giant Velosiped", 5000000, 4500000, "Velosipedlar"),
            ("Merida Velosiped", 4000000, 3500000, "Velosipedlar"),
            ("O'tgan Kunlar", 150000, 120000, "Badiiy adabiyot"),
            ("Python dasturlash", 300000, 250000, "Dasturlash"),
            ("JavaScript asoslari", 280000, 230000, "Dasturlash"),
            ("Bolalar ertaklari", 100000, 80000, "Bolalar kitoblari"),
            ("Olma", 30000, 25000, "Mevalar"),
            ("Banan", 25000, 20000, "Mevalar"),
            ("Kartoshka", 15000, 12000, "Sabzavotlar"),
            ("Piyoz", 10000, 8000, "Sabzavotlar"),
            ("Nestle Sut", 15000, 12000, "Sut mahsulotlari"),
            ("Sut mahsulotlari to'plami", 50000, 45000, "Sut mahsulotlari"),
            ("Non", 8000, 7000, "Non mahsulotlari"),
            ("Lavash", 6000, 5000, "Non mahsulotlari"),
            ("Coca Cola", 5000, 4000, "Ichimliklar"),
            ("Fanta", 5000, 4000, "Ichimliklar"),
            ("Shokolad", 15000, 12000, "Shirinliklar"),
            ("Pechnye", 10000, 8000, "Shirinliklar"),
            ("Lavazza Qahva", 50000, 45000, "Qahva"),
            ("Ahmad Choy", 30000, 25000, "Choy"),
            ("Yoshil choy", 25000, 20000, "Choy"),
            ("Mobil telefon aksessuarlari", 200000, 150000, "Aksessuarlar"),
            ("Kabel va adapterlar", 150000, 120000, "Aksessuarlar"),
        ]

        self.stdout.write('Generating products...')
        for i, (name, price, discount_price, category_name) in enumerate(products_data):
            try:
                category = Category.objects.get(name=category_name)
                Product.objects.get_or_create(
                    name=name,
                    defaults={
                        'category': category,
                        'price': price,
                        'discount_price': discount_price,
                        'description': f'{name} - sifatli mahsulot. Eng yaxshi narxlarda.',
                        'status': True,
                        'count': random.randint(10, 100)
                    }
                )
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Category {category_name} not found, skipping {name}'))

        self.stdout.write(self.style.SUCCESS(f'Generated {len(products_data)} products'))
