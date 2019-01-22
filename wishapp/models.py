from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404


class Wish(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wish'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )
    total_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return ' '.join((self.user.username, self.product.title))

    def add(request, pk):
        product = get_object_or_404(Product, pk=pk)
        wish_item = Wish.objects.filter(user=request.user, product=product)
        if not wish_item:
            wish_item = Wish(user=request.user, product=product)
            wish_item.save()

    def remove(request, pk):
        product = get_object_or_404(Product, pk=pk)
        wish_item = Wish.objects.get(user=request.user, product=product)
        wish_item.delete()
