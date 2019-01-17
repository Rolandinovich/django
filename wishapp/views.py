from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from wishapp.models import Wish, add, remove
from cartapp.models import Cart
from mainapp.models import Product, get_menu
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def wish(request):
    context = {'menu': get_menu(),
               'wish': Wish.objects.filter(user=request.user),
               'cart': Cart.objects.filter(user=request.user),
               }
    return render(request, 'wishapp/wish.html', context)


def wish_add(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    add(request, pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def wish_remove(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    remove(request, pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
