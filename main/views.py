
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from . import models
from django.contrib.auth import authenticate, login, logout


def index(request):
    categories = models.Category.objects.filter()[:10]
    top_categories = models.Category.objects.all()[:7]
    products = models.Product.objects.all()

    query = request.GET.get('query')
    if query:
        products = products.filter(name__icontains=query)

    featured_products = models.Product.objects.filter(
        discount_price__isnull=False
    ).exclude(discount_price=0)[:8]

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'categories': categories,
        'top_categories' :top_categories,
        'products' :products,
        'featured_products': featured_products,
        'total_products': models.Product.objects.count(),
        'total_categories': models.Category.objects.count(),
        'total_orders': models.Cart.objects.exclude(status=1).count(),
        'wishlist_ids': wishlist_ids,
        'query': query
    }

    return render(request, 'front/index.html', context=context)



def product_detail(request, code):
    product = models.Product.objects.get(code=code)
    if product.category:
        related_products = models.Product.objects.filter(category=product.category).exclude(code=code)[:8]
    else:
        related_products = []

    reviews = models.Review.objects.filter(product=product).order_by('-created_at')
    if request.user.is_authenticated:
        wishlist_ids = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        wishlist_ids = []

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()
        if rating and comment:
            models.Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, "Sharhingiz muvaffaqiyatli saqlandi.")
            return redirect('product_detail', code=code)
        messages.error(request, "Iltimos, yulduzcha va sharhni kiriting.")

    context = {
        "product": product,
        "related_products": related_products,
        "wishlist_ids": wishlist_ids,
        "reviews": reviews,
    }

    return render(request, 'front/detail.html', context=context)


def category_filter(request, category_id):
    products = models.Product.objects.filter(category_id=category_id)

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'products': products,
        'wishlist_ids': wishlist_ids
    }
    return render(request, 'front/category_filter.html', context)

def all_products(request):
    products = models.Product.objects.all()
    categories = models.Category.objects.all()
    top_categories = models.Category.objects.all()[:7]

    category_id = request.GET.get('category')
    active_category = None
    active_category_name = None

    if category_id:
        products = products.filter(category_id=category_id)
        active_category = int(category_id)
        try:
            active_category_name = models.Category.objects.get(id=category_id).name
        except models.Category.DoesNotExist:
            active_category_name = "Category"

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)

    context = {
        'products': products,
        'categories': categories,
        'top_categories': top_categories,
        'active_category': active_category,
        'active_category_name': active_category_name,
        'total_products': models.Product.objects.count(),
        'current_sort': sort,
        'wishlist_ids': wishlist_ids
    }

    return render(request, 'front/category_filter.html', context)


# --------------------AUTH------------------------------
def register(request):
    if request.method =="POST":
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            models.User.objects.create_user(username, phone, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

        else:
            return render(request, 'front/register.html')

    return  render(request, 'front/register.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
    return render(request, 'front/login.html')

def log_out(request):
    logout(request)
    return redirect('index')



@login_required(login_url='login')
def profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get('username')
        user.last_name = request.POST.get('last_name')
        user.first_name = request.POST.get('first_name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        if request.FILES.get('photo'):
            user.photo = request.FILES.get('photo')

        user.save()

    orders = models.Cart.objects.filter(user=request.user).exclude(status=1).order_by('-id')
    return render(request,  'front/profile.html', {'orders': orders})


@login_required(login_url='login')
def my_orders(request):
    orders = models.Cart.objects.filter(user=request.user).exclude(
        status=1
    ).prefetch_related('cartproduct_set__product').order_by('-id')
    context = {
        'orders': orders,
    }
    return render(request, 'front/orders.html', context=context)


@login_required(login_url='login')
def cancel_order(request, cart_code):
    if request.method != 'POST':
        return redirect('my_orders')

    cart = models.Cart.objects.filter(code=cart_code, user=request.user).first()
    if not cart or cart.status not in (2, 3):
        messages.error(request, "Bu buyurtmani bekor qilib bo'lmaydi.")
        return redirect('my_orders')

    # Mahsulotlar omborga qaytariladi
    for item in cart.cartproduct_set.all():
        if item.product:
            item.product.count += item.count
            item.product.save()

    cart.status = 5
    cart.delivery_date = None
    cart.save()
    messages.success(request, "Buyurtma bekor qilindi.")
    return redirect('my_orders')


@login_required(login_url='login')
def delete_order(request, cart_code):
    if request.method != 'POST':
        return redirect('my_orders')

    cart = models.Cart.objects.filter(
        code=cart_code, user=request.user, status=5
    ).first()
    if not cart:
        messages.error(request, "Faqat bekor qilingan buyurtmani o'chirish mumkin.")
    else:
        cart.delete()
        messages.success(request, "Buyurtma o'chirildi.")
    return redirect('my_orders')


@login_required(login_url='login')
def add_wishlist(request, product_code):
    product = models.Product.objects.get(code=product_code)
    element = models.WishList.objects.filter(product=product, user=request.user)
    if not element:
        models.WishList.objects.create(product=product, user=request.user)
    return redirect('index')

@login_required(login_url='login')
def delete_wishlist(request, product_code):
    product = models.Product.objects.get(code=product_code)
    element = models.WishList.objects.filter(product=product, user=request.user)
    if element:
        element.delete()
        return redirect('index')
    return redirect('index')



@login_required(login_url='login')
def wishlist(request):
    wishlist_products = models.WishList.objects.filter(user=request.user)
    context = {
        "wishlist_products" :wishlist_products
    }
    return render(request, 'front/wishlist.html', context=context)
@login_required(login_url='login')
def cart(request):
    cart = models.Cart.objects.filter(user=request.user ,status=1).first()
    if not cart:
        cart = models.Cart.objects.create(user=request.user ,status=1)
    cart_product =models.CartProduct.objects.filter(cart=cart)
    context ={
        'cart_products' :cart_product,
    }
    return render(request, 'front/cart.html', context=context)
@login_required(login_url='login')
def add_to_cart(request ,product_code):
    product =models.Product.objects.get(code=product_code)
    cart =models.Cart.objects.filter(user=request.user ,status=1).first()
    if not cart:
        cart =models.Cart.objects.create(user=request.user ,status=1)

    quantity = int(request.GET.get('quantity', 1))
    cart_product =models.CartProduct.objects.filter(cart=cart ,product=product).first()
    if cart_product:
        cart_product.count += quantity
        cart_product.save_snapshot()
        cart_product.save()
    else:
        cart_product =models.CartProduct.objects.create(cart=cart ,product=product ,count=quantity)
        cart_product.save_snapshot()
        cart_product.save()
    return redirect('cart')
@login_required(login_url='login')
def cart_product_count_plus(request ,cart_product_code):
    cart_product =models.CartProduct.objects.get(code=cart_product_code)
    cart_product.count += 1
    cart_product.save()
    from django.http import JsonResponse
    return JsonResponse({
        'success': True,
        'new_count': cart_product.count,
        'total_price': str(cart_product.total_price)
    })
@login_required(login_url='login')
def cart_product_count_minus(request ,cart_product_code):
    from django.http import JsonResponse
    cart_product =models.CartProduct.objects.get(code=cart_product_code)
    if cart_product.count > 1:
        cart_product.count -= 1
        cart_product.save()
        return JsonResponse({
            'success': True,
            'new_count': cart_product.count,
            'total_price': str(cart_product.total_price)
        })
    else:
        cart_product.delete()
        return JsonResponse({
            'success': True,
            'new_count': 0,
            'total_price': '0'
        })

@login_required(login_url='login')
def cart_personal(request):
    cart = models.Cart.objects.filter(user=request.user, status=1).first()
    context = {
        'cart' :cart
    }
    if request.method == 'POST':
        request.user.username = request.POST['username']
        request.user.address = request.POST['address']
        request.user.phone = request.POST['phone']
        request.user.save()
        return redirect('cart_personal')


    return render(request, 'front/cart-personal.html', context=context)


@login_required(login_url='login')
def order(request, cart_code):
    cart = models.Cart.objects.get(code=cart_code)
    cart_products = models.CartProduct.objects.filter(cart=cart)
    for i in cart_products:
        i.save_snapshot()
        if i.product:
            i.product.count -= i.count
            i.product.save()
        i.save()
    cart.status = 2
    cart.save()
    return redirect('thank_you_cart', cart_code=cart_code)


def thank_you(request, cart_code=None):
    cart = None
    cart_products = []
    if cart_code:
        try:
            cart = models.Cart.objects.get(code=cart_code)
            cart_products = models.CartProduct.objects.filter(cart=cart).select_related('product')
        except models.Cart.DoesNotExist:
            pass
    context = {
        'cart': cart,
        'cart_products': cart_products,
    }
    return render(request, 'front/thank-you.html', context=context)
