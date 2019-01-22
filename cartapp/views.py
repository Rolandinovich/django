from django.shortcuts import HttpResponseRedirect
from cartapp.models import Cart
from wishapp.models import Wish
from cartapp.forms import CartQuantityForm
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class CartListView(LoginRequiredMixin, ListView):
    model = Cart

    def get_context_data(self, **kwargs):
        data = super(CartListView, self).get_context_data(**kwargs)
        data['cart'] = Cart.objects.filter(user=self.request.user)
        data['wish'] = Wish.objects.filter(user=self.request.user)
        return data

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


def cart_add(request, pk, add_quantity=0):
    if not add_quantity:
        if request.method == 'POST' and CartQuantityForm(data=request.POST).is_valid():
            add_quantity = int(request.POST['quantity'])
        else:
            add_quantity = 1

    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            ''.join([reverse('accounts:login'),
                     '?next=', request.META.get('HTTP_REFERER'),
                     '&action=', request.get_full_path() + str(add_quantity) + '/'])
        )

    Cart.add_to_card(request, pk, add_quantity)

    link_next_page = request.GET['next'] if 'next' in request.GET.keys() else ''
    if link_next_page:
        return HttpResponseRedirect(link_next_page)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            ''.join([reverse('accounts:login'),
                     '?next=', request.META.get('HTTP_REFERER'),
                     '&action=', request.get_full_path()])
        )

    Cart.remove_from_card(request, pk)

    link_next_page = request.GET['next'] if 'next' in request.GET.keys() else ''
    if link_next_page:
        return HttpResponseRedirect(link_next_page)
    else:
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
            'object_list': cart_items,
        }

        result = render_to_string('cartapp/cart_items.html', content)

        return JsonResponse({'result': result})
