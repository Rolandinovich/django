from django.shortcuts import HttpResponseRedirect
from wishapp.models import Wish
from cartapp.models import Cart
from django.urls import reverse
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


def wish_add(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            ''.join([reverse('accounts:login'),
                     '?next=', request.META.get('HTTP_REFERER'),
                     '&action=', request.get_full_path()])
        )

    Wish.add(request, pk)

    link_next_page = request.GET['next'] if 'next' in request.GET.keys() else ''
    if link_next_page:
        return HttpResponseRedirect(link_next_page)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def wish_remove(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:login'))
    Wish.remove(request, pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
