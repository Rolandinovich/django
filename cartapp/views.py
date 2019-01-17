from django.shortcuts import render, HttpResponseRedirect
from cartapp.models import Cart, add_to_card, remove_from_card
from wishapp.models import Wish
from cartapp.forms import CartQuantityForm
from mainapp.models import get_menu
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse


# Create your views here.

@login_required
def cart_ajax(request):
    context = {'menu': get_menu(),
               'wish': Wish.objects.filter(user=request.user),
               'cart': Cart.objects.filter(user=request.user),
               }
    return render(request, 'cartapp/cart_ajax.html', context)


def cart_add(request, pk):
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    ADD_QUANTITY = int(request.GET['quantity'] if 'quantity' in request.GET.keys() else '0')
    cart_quantity = CartQuantityForm(data=request.POST)
    if not ADD_QUANTITY:
        if cart_quantity.is_valid():
            ADD_QUANTITY = int(request.POST['quantity'])
        else:
            ADD_QUANTITY = 1
    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            ''.join([reverse('accounts:login'),
                     '?next=', request.META.get('HTTP_REFERER'),
                     '&action=', request.get_full_path(),
                     '&quantity=', str(ADD_QUANTITY)])
        )

    add_to_card(request, pk, ADD_QUANTITY)

    if next:
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    remove_from_card(request, pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_cart_item = Cart.objects.get(pk=int(pk))

        if quantity > 0:
            new_cart_item.quantity = quantity
            new_cart_item.save()
        else:
            new_cart_item.delete()

        cart_items = Cart.objects.filter(user=request.user).order_by('product__category')

        content = {
            'cart': cart_items,
        }

        result = render_to_string('cartapp/cart_list.html', content)

        return JsonResponse({'result': result})
