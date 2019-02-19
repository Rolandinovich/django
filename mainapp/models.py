from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404


# Формирование меню слева
def get_menu():
    def get_links_menu():
        links = []
        for m in Menu.objects.all().select_related():
            submenu = []
            for sm in Menu_element.objects.filter(menu__title=m.title).select_related():
                submenu.append({'title': sm.category.title, 'pk': sm.pk})
            links.append({'title': m.title, 'submenu': submenu})
        return links

    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = get_links_menu()
            cache.set(key, links_menu)
        return links_menu
    else:
        return get_links_menu()


class Menu(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
    )

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
    )
    snippet = models.TextField(
        blank=True,
        null=True,
    )
    modified = models.DateTimeField(
        auto_now=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(db_index=True, verbose_name='активна', default=True)

    def __str__(self):
        return self.title


class Menu_element(models.Model):
    class Meta:
        unique_together = (("menu", "category"),)

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return ' '.join((self.menu.title, self.category.title))


class Product(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
    )
    category = models.ForeignKey(
        Category,
        related_name='product_set',
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='products_images',
        blank=True,
        null=True,
        verbose_name='Фото1')
    image2 = models.ImageField(
        upload_to='products_images',
        blank=True,
        null=True,
        verbose_name='Фото2')

    shortdescription = models.TextField(
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    oldcost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    new = models.BooleanField(
        default=True
    )
    quantity = models.IntegerField(verbose_name='количество',
                                   default=0)
    modified = models.DateTimeField(
        auto_now=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(db_index=True, verbose_name='активнен', default=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'title')


# 3  специальных предложения с таймером
class Hotdial(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    date_end = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.product.title


# 3 новости слайдера под поиском на главной странице

class Three_slide_news(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    title1 = models.CharField(
        max_length=250
    )
    title2 = models.CharField(
        max_length=250
    )

    image = models.ImageField(
        upload_to='Three_slide_news_images',
        blank=True,
        null=True,
        verbose_name='Фото')

    def __str__(self):
        return self.product.title


# Специальные предложения "новые товары", "скидки", "top sellers" для первой страницы

class Special_offers(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    new = models.BooleanField(
        default=True
    )
    sale = models.BooleanField(
        default=True
    )

    best_selling = models.BooleanField(
        default=True
    )

    def __str__(self):
        return ' '.join(("new=", str(self.new), "sale=", str(self.sale), "best_selling=",
                         str(self.best_selling), self.product.title))


def get_context_main_view():
    if settings.LOW_CACHE:
        key = 'hot_links'
        hot_links = cache.get(key)
        if hot_links is None:
            hot_links = {'new_products': Special_offers.objects.filter(new=True).select_related(),
                         'sale_products': Special_offers.objects.filter(sale=True).select_related(),
                         'best_selling_products': Special_offers.objects.filter(best_selling=True).select_related(),
                         'hot_dials': Hotdial.objects.all().select_related(),
                         'three_slide_news': Three_slide_news.objects.all().select_related(),
                         }
            cache.set(key, hot_links)
        return hot_links
    else:
        return {'new_products': Special_offers.objects.filter(new=True).select_related(),
                'sale_products': Special_offers.objects.filter(sale=True).select_related(),
                'best_selling_products': Special_offers.objects.filter(best_selling=True).select_related(),
                'hot_dials': Hotdial.objects.all().select_related(),
                'three_slide_news': Three_slide_news.objects.all().select_related(),
                }


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(Category, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(Category, pk=pk)


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)
