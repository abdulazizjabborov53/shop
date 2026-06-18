
from django.shortcuts import render,redirect
from main import models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.timezone import now
from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def index(request):
    # Get sales data
    sales = (
        models.CartProduct.objects
        .filter(cart__status=4)
        .annotate(month=TruncMonth('cart__date'))
        .values('month')
        .annotate(
            total=Sum(F('product__price') * F('count')),
            discount=Sum(
                (F('product__price') - F('product__discount_price')) * F('count')
            )
        )
        .order_by('month')
    )

    totals = [float(d['total'] or 0) for d in sales]

    stats = {
        'total_customers': models.User.objects.count(),
        'total_income': sum(totals),
        'completed_orders': models.Cart.objects.filter(status=4).count(),
        'new_customers': models.User.objects.filter(
            date_joined__month=now().month
        ).count(),
        'pending_orders': models.Cart.objects.filter(status=1).count(),
        'total_orders': models.Cart.objects.count(),
    }

    return render(request, 'dashboard/index.html', {'stats': stats})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def create_category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            logo = request.FILES.get('logo')
            if not name or not logo:
                messages.warning(request, 'Barcha maydonlarni toldirish shart')
                return redirect('d_create_category')
            category = models.Category.objects.create(name=name, logo=logo)
            messages.success(request, 'Categorya yaratildi')
            return redirect('d_index')
        except Exception as e:
            messages.error(request, 'Xatolik')
            return redirect('d_create_category')
    return render(request, 'dashboard/create_category.html')

@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def list_category(request):
    query = request.GET.get('query')
    categories = models.Category.objects.all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'dashboard/category_list.html', {'categories': categories, 'query': query})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def product_list(request):
    query = request.GET.get('query')
    products = models.Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'dashboard/product_list.html', {'products': products, 'query': query})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def create_product(request):
    categories = models.Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        if discount_price == '':
            discount_price = None
        status = request.POST.get('status') == 'on'
        count = request.POST.get('count')
        category=request.POST.get('category')
        Product = models.Product.objects.create(
            name=name, 
            description=description, 
            image=image,
            price=price,
            category_id=category,
            discount_price=discount_price, 
            count=count,
        )
        messages.success(request, 'Product yaratildi')
        return redirect('d_list_product')
    
    return render(request, 'dashboard/product_create.html', {'categories': categories})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def edit_category(request, id):
    category = models.Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        status = request.POST.get('is_active')
        if status:
            category.is_active = True
        else:
            category.is_active = False

        logo = request.FILES.get('logo')
        if logo:
            category.logo = logo
        category.save()
        messages.success(request, 'Categorya yangilandi')
        return redirect('d_list_category')

    context = {'category': category}
    return render(request, 'dashboard/edit_category.html',context=context)

@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def delete_category(request, id):
    category = models.Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Categorya o\'chirildi')
    return redirect('d_list_category')
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')

def delete_product(request, id):
    product = models.Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product o\'chirildi')
    return redirect('d_list_product')
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def edit_product(request, id):
    product = models.Product.objects.get(id=id)
    categories = models.Category.objects.all()
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        discount_price = request.POST.get('discount_price')
        if discount_price == '':
            discount_price = None
        product.discount_price = discount_price
        product.status = request.POST.get('status') == 'on'
        product.count = request.POST.get('count')
        product.category_id = request.POST.get('category')
        
        image = request.FILES.get('image')
        if image:
            product.image = image
        
        product.save()
        messages.success(request, 'Product yangilandi')
        return redirect('d_list_product')
    
    context = {'product': product, 'categories': categories}
    return render(request, 'dashboard/edit_product.html', context=context)
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    return render(request, 'dashboard/product_detail.html', {'product': product})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def category_detail(request, id):
    category = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=category)
    return render(request, 'dashboard/category_detail.html', {'category': category, 'products': products})

@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def orders(request):
    query = request.GET.get('query')
    order = models.Cart.objects.all().order_by('-id')
    if query:
        order = order.filter(
            Q(code__icontains=query) |
            Q(cartproduct__product__name__icontains=query) |
            Q(cartproduct__product__code__icontains=query)
        ).distinct()

    return render(request, 'dashboard/order_list.html', {'orders': order, "query": query})

@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def status_update(request, code):
    order = models.Cart.objects.get(code=code)
    if order.status <= 4:
        order.status = order.status + 1
        order.save()
        messages.success(request, 'Status o`zgartirildi')
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('d_orders')
    messages.error(request, 'Xatolik')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('d_orders')


@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def reject_cart(request, code):
    order = models.Cart.objects.filter(code=code).first()
    if order.status >1:
        order.status = order.status - 1
        order.save()
        messages.success(request, 'Qaytarildi')
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('d_orders')
    messages.error(request, 'Xatolik')
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('d_orders')


@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def yolda_orders(request):
    orders = models.Cart.objects.filter(status=3)
    return render(request, 'dashboard/yolda_orders.html', {'orders': orders})

@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def yigilmoqda_orders(request):
    orders = models.Cart.objects.filter(status=2)

    return render(request, 'dashboard/yigilmoqda_orders.html', {'orders': orders})
@user_passes_test(lambda u: u.is_superuser,login_url='d_login')
def cart_detail(request, code):
    order = models.Cart.objects.get(code=code)
    cart_products = models.CartProduct.objects.filter(cart=order)

    context = {
                'order': order,
               'cart_products': cart_products,
    }
    return render(request, 'dashboard/orders_detail.html', context=context)

def log_in(request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password, is_staff=True)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('d_index')
            messages.error(request, 'Xatolik')
            return redirect('d_login')

        return render(request, 'dashboard/login.html')

@user_passes_test(lambda u: u.is_superuser, login_url='d_login')


def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        
        photo = request.FILES.get('photo')
        if photo:
            user.photo = photo
        
        user.save()
        messages.success(request, 'Profil muvaffaqiyatli yangilandi')
        return redirect('d_profile')
    
    orders = models.Cart.objects.filter(user=request.user).order_by('-id')
    return render(request, 'dashboard/profile.html', {'orders': orders})

def log_out(request):
    logout(request)
    messages.success(request, 'Tizimdan chiqdingiz')
    return redirect('d_login')

@user_passes_test(lambda u: u.is_superuser, login_url='d_login')
def enter_product_list(request):
    enter_products = models.EnterProduct.objects.all()
    return render(request, 'dashboard/enter_product_list.html', {'enter_products': enter_products})

@user_passes_test(lambda u: u.is_superuser, login_url='d_login')
def create_enter_product(request):
    products = models.Product.objects.all()
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        count = int(request.POST.get('count'))
        models.EnterProduct.objects.create(
            product_id=product_id,
            count=count
        )
        messages.success(request, 'EnterProduct yaratildi')
        return redirect('d_list_enter_product')
    
    return render(request, 'dashboard/enter_product_create.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser, login_url='d_login')
def edit_enter_product(request, id):
    enter_product = models.EnterProduct.objects.get(id=id)
    products = models.Product.objects.all()
    
    if request.method == 'POST':
        enter_product.product_id = request.POST.get('product')
        enter_product.count = int(request.POST.get('count'))
        enter_product.save()
        messages.success(request, 'EnterProduct yangilandi')
        return redirect('d_list_enter_product')
    
    return render(request, 'dashboard/enter_product_edit.html', {'enter_product': enter_product, 'products': products})

from django.utils.timezone import now
# views.py
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse

def revenue_chart_data(request):
    # Cart_total_price - yetkazilgan buyurtmalar
    sales = (
        models.CartProduct.objects
        .filter(cart__status=4)
        .annotate(month=TruncMonth('cart__date'))
        .values('month')
        .annotate(
            total=Sum(F('product__price') * F('count')),
            discount=Sum(
                (F('product__price') - F('product__discount_price')) * F('count')
            )
        )
        .order_by('month')
    )

    labels = [d['month'].strftime('%B') for d in sales]
    totals = [float(d['total'] or 0) for d in sales]
    discounts = [float(d['discount'] or 0) for d in sales]

    stats = {
        'total_customers': models.User.objects.count(),
        'total_income': sum(totals),
        'completed_orders': models.Cart.objects.filter(status=4).count(),
        'new_customers': models.User.objects.filter(
            date_joined__month=now().month
        ).count(),
    }

    return JsonResponse({'labels': labels, 'totals': totals,
                         'discounts': discounts, 'stats': stats})