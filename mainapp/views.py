import json
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator
from mainapp.models import Menu, Menu_element, Category, Product, Hotdial, Three_slide_news, Special_offers, get_menu
from cartapp.models import Cart
from cartapp.forms import CartQuantityForm
from wishapp.models import Wish
from django.urls import reverse_lazy, reverse


# Create your views here.


def main_view(request):
    context = {'new_products': Special_offers.objects.filter(new=True),
               'sale_products': Special_offers.objects.filter(sale=True),
               'best_selling_products': Special_offers.objects.filter(best_selling=True),
               'hot_dials': Hotdial.objects.all(),
               'three_slide_news': Three_slide_news.objects.all()
               }
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })
    return render(request, 'mainapp/index.html', context)


def about_view(request):
    context = {}
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })
    return render(request, 'mainapp/about.html', context)


def contact_view(request):
    if request.user.is_authenticated:
        context = {'cart': Cart.objects.filter(user=request.user),
                   'wish': Wish.objects.filter(user=request.user),
                   }
    return render(request, 'mainapp/contact.html', context)


def product_details_view(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })
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
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })
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
    if request.user.is_authenticated:
        context.update({'cart': Cart.objects.filter(user=request.user),
                        'wish': Wish.objects.filter(user=request.user),
                        })
    return render(request, 'mainapp/search.html', context)
