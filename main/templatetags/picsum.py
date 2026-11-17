from django import template

register = template.Library()

# Har bir mahsulot uchun picsum.photos rasm ID'si.
# Rasmlarni ko'rish va boshqasini tanlash: https://picsum.photos/images
# ID raqamini o'zgartirsangiz, o'sha mahsulotning rasmi o'zgaradi.
PRODUCT_IMAGES = {
    47: 0,    # Laptop Pro 15          -> noutbuk
    48: 529,  # Simsiz Quloqchin       -> dinamik / audio
    49: 175,  # Smart Soat T8          -> soat
    50: 856,  # Erkaklar Ko'ylagi      -> erkaklar kiyimi
    51: 473,  # Sport Kostyumi         -> sport kiyimi
    52: 113,  # Qozon To'plami         -> qozon
    53: 1,    # Python Asoslari        -> noutbuk / dasturlash
    54: 292,  # Futbol To'pi           -> to'p
}

# Kategoriyalar uchun picsum.photos rasm ID'si.
CATEGORY_IMAGES = {
    21: 367,  # Elektronika
    22: 661,  # Kiyim-kechak
    23: 307,  # Uy jihozlari
    24: 1073, # Kitoblar
    25: 31,   # Sport buyumlari
}

# Ro'yxatda yo'q (yangi qo'shilgan) mahsulotlar uchun zaxira rasmlar.
FALLBACK_IDS = [0, 1, 2, 3, 20, 21, 30, 42, 60, 96, 160, 180, 237, 250, 292, 431]


def _picsum_url(image_id, size):
    return f'https://picsum.photos/id/{image_id}/{size}/{size}'


@register.filter
def picsum(product_id, size=400):
    """Mahsulot ID'siga mos, har doim bir xil ochiladigan picsum rasm URL'i."""
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        product_id = 0

    image_id = PRODUCT_IMAGES.get(product_id)
    if image_id is None:
        image_id = FALLBACK_IDS[product_id % len(FALLBACK_IDS)]

    return _picsum_url(image_id, size)


@register.filter
def cat_picsum(category_id, size=100):
    """Kategoriya ID'siga mos picsum rasm URL'i."""
    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        category_id = 0

    image_id = CATEGORY_IMAGES.get(category_id)
    if image_id is None:
        image_id = FALLBACK_IDS[category_id % len(FALLBACK_IDS)]

    return _picsum_url(image_id, size)
