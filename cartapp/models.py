from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator
from django.utils.functional import cached_property


class CartQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(CartQuerySet, self).delete(*args, **kwargs)


class Cart(models.Model):
    objects = CartQuerySet.as_manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=1,
        validators=[MinValueValidator(1)]
    )

    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )

    def __str__(self):
        return ' '.join((self.user.username, self.product.title))

    def _get_product_cost(self):
        return self.product.cost * self.quantity

    product_cost = property(_get_product_cost)

    @cached_property
    def get_items_cached(self):
        return self.user.cart.select_related()

    def _get_total_quantity(self):
        # _items = Cart.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        # _items = Cart.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    total_cost = property(_get_total_cost)


    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.objects.get(pk=self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    # Добавление товара в корзину

    def add_to_card(request, pk, ADD_QUANTITY):
        product = get_object_or_404(Product, pk=pk)
        old_cart_item = Cart.objects.filter(user=request.user, product=product)
        if old_cart_item:
            old_cart_item[0].quantity += ADD_QUANTITY
            old_cart_item[0].save()
        else:
            new_cart_item = Cart(user=request.user, product=product)
            new_cart_item.quantity = ADD_QUANTITY
            new_cart_item.save()

    # Удаление товара из корзины
    def remove_from_card(request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart_item = Cart.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
