from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from wishapp.models import Wish, add, remove
from cartapp.models import Cart
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class WishListView(LoginRequiredMixin, ListView):
    model = Wish

    def get_context_data(self, **kwargs):
        data = super(WishListView, self).get_context_data(**kwargs)
        data['cart'] = Cart.objects.filter(user=self.request.user)
        data['wish'] = Wish.objects.filter(user=self.request.user)
        return data

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user)


# @login_required
# def wish(request):
#     context = {'menu': get_menu(),
#                'wish': Wish.objects.filter(user=request.user),
#                'cart': Cart.objects.filter(user=request.user),
#                }
#     return render(request, 'wishapp/wish_list.html', context)


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
