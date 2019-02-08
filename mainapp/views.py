from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from mainapp.models import Product, get_context_main_view, get_category, get_product
from wishapp.models import Wish
from cartapp.models import Cart
from cartapp.forms import CartQuantityForm
from django.views.decorators.cache import cache_page, never_cache


# Create your views here.

@cache_page(3600)
def main_view(request):
    return render(request, 'mainapp/index.html', get_context_main_view())


@cache_page(3600)
def about_view(request):
    return render(request, 'mainapp/about.html')


@cache_page(3600)
def contact_view(request):
    return render(request, 'mainapp/contact.html')


@cache_page(3600)
def product_details_view(request, pk):
    return render(request, 'mainapp/product-details.html', {'product': get_product(pk)})


@cache_page(3600)
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
        category = get_category(pk)
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
    return render(request, 'mainapp/search.html', context)


@never_cache
def get_user_content_ajax(request):
    """Функция возвращает корректные данные для меню пользователя и выпадающей корзины
    используется при общем кэшировании контроллера"""
    if request.is_ajax():
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).select_related
            wish = Wish.objects.filter(user=request.user)
        else:
            cart = None
            wish = None
        top_cart = render_to_string('mainapp/master_pages/inc_mini_cart_content.html',
                                    {'cart': cart})
        user_menu = render_to_string('mainapp/master_pages/inc_user_menu.html',
                                     {'user': request.user, 'wish': wish})
        return JsonResponse({'top_cart': top_cart, 'user_menu': user_menu})
