from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from mainapp.models import Category, Product, Hotdial, Three_slide_news, Special_offers
from cartapp.models import Cart
from cartapp.forms import CartQuantityForm
from wishapp.models import Wish


# Create your views here.

def add_page_objects_if_user_is_authenticated(request, context):
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })


def main_view(request):
    context = {'new_products': Special_offers.objects.filter(new=True),
               'sale_products': Special_offers.objects.filter(sale=True),
               'best_selling_products': Special_offers.objects.filter(best_selling=True),
               'hot_dials': Hotdial.objects.all(),
               'three_slide_news': Three_slide_news.objects.all()
               }
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/index.html', context)


def about_view(request):
    context = {}
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/about.html', context)


def contact_view(request):
    context = {}
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/contact.html', context)


def product_details_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/product-details.html', context)


def products_view(request, pk=0, special=''):
    cart_quantity = CartQuantityForm()
    if special == 'all':
        products = Product.objects.all()
        category_title = 'Все продукты'
    if special == 'new':
        products = Product.objects.filter(new=True)
        category_title = 'Новое поступление'
    if special == 'sale':
        products = Product.objects.filter(oldcost__gt=0)
        category_title = 'Лучшие предложения'
    if pk:
        category = get_object_or_404(Category, pk=pk)
        products = Product.objects.filter(category__pk=pk)
        category_title = category.title
    ITEMS_COUNT_ON_PAGE = 4
    paginator = Paginator(products, ITEMS_COUNT_ON_PAGE)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {'products': items,
               'cart_quantity': cart_quantity,
               'category_title': category_title,
               }
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/products.html', context)


def products_search(request):
    cart_quantity = CartQuantityForm()
    category_title = 'Поиск'
    ITEMS_COUNT_ON_PAGE = 4
    option = request.GET.get('option')
    search_str = request.GET.get('search_str')
    if option == 'Все категории':
        products = Product.objects.all().filter(title__icontains=search_str)
    else:
        products = Product.objects.filter(category__title=option).filter(title__icontains=search_str)
    paginator = Paginator(products, ITEMS_COUNT_ON_PAGE)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    context = {'products': items,
               'cart_quantity': cart_quantity,
               'category_title': category_title,
               'option': option,
               'search_str': search_str,
               }
    add_page_objects_if_user_is_authenticated(request, context)
    return render(request, 'mainapp/search.html', context)
