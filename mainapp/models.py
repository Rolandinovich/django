from django.db import models


# Формирование меню слева
def get_menu():
    main_menu = []
    for m in Menu.objects.all():
        submenu = []
        for sm in Menu_element.objects.filter(menu__title=m.title):
            submenu.append({'title': sm.category.title, 'pk': sm.pk})
        main_menu.append({'title': m.title, 'submenu': submenu})
    return main_menu


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

    is_active = models.BooleanField(verbose_name='активна', default=True)

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

    is_active = models.BooleanField(verbose_name='активнен', default=True)

    def __str__(self):
        return self.title


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
