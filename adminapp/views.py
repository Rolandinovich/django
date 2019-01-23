from django.shortcuts import render, get_object_or_404
from accounts.models import Account
from mainapp.models import Category, Product
from ordersapp.models import Order
from django.contrib.auth.decorators import user_passes_test
from accounts.forms import AccountRegisterForm
from adminapp.forms import AccountAdminEditForm, CategoryEditForm, ProductEditForm
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


class UsersListView(ListView):
    model = Account
    template_name = 'adminapp/users.html'

    def get_context_data(self, **kwargs):
        data = super(UsersListView, self).get_context_data(**kwargs)
        data['title'] = 'Пользователи'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UsersListView, self).dispatch(*args, **kwargs)


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        data = super(CategoryCreateView, self).get_context_data(**kwargs)
        data['title'] = 'Создание категории'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(*args, **kwargs)


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Категория/Редактирование'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Удаление категории'

        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(*args, **kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Продукт/Подробная информация'

        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductDetailView, self).dispatch(*args, **kwargs)


class UserCreateView(CreateView):
    model = Account
    template_name = 'adminapp/user_update.html'
    form_class = AccountRegisterForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        data = super(UserCreateView, self).get_context_data(**kwargs)
        data['title'] = 'Пользователи/Создание'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)


class UserUpdateView(UpdateView):
    model = Account
    template_name = 'adminapp/user_update.html'
    form_class = AccountAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        data = super(UserUpdateView, self).get_context_data(**kwargs)
        data['title'] = 'Пользователь/Редактирование'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)


class UserDeleteView(DeleteView):
    model = Account
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        data = super(UserDeleteView, self).get_context_data(**kwargs)
        data['title'] = 'Пользователь/Удаление'
        return data

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(*args, **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'adminapp/categories.html'

    def get_context_data(self, **kwargs):
        data = super(CategoryListView, self).get_context_data(**kwargs)
        data['title'] = 'Категории'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CategoryListView, self).dispatch(*args, **kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    success_url = reverse_lazy('adminapp:products')

    def get_context_data(self, **kwargs):
        data = super(ProductListView, self).get_context_data(**kwargs)
        data['title'] = 'Категория/Продукты'
        data['object_list'] = Product.objects.filter(category__pk=self.kwargs.get('pk'))
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        data['category'] = category
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductListView, self).dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        data = super(ProductCreateView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        data['category'] = category
        data['title'] = 'Категория/Добавление продукта'
        if not self.request.method == 'POST':
            form = ProductEditForm(initial={'category': category})
            data['form'] = form
        return data

    def get_success_url(self):
        return reverse_lazy('adminapp:products', kwargs={'pk': self.kwargs['pk']})

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductCreateView, self).dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        data = super(ProductUpdateView, self).get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        data['category'] = product.category
        data['title'] = 'Категория/Редактирование продукта'
        return data

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return reverse_lazy('adminapp:products', kwargs={'pk': product.category.pk})

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductUpdateView, self).dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_context_data(self, **kwargs):
        data = super(ProductDeleteView, self).get_context_data(**kwargs)
        data['title'] = 'Продукт/Удаление'
        return data

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return reverse_lazy('adminapp:products', kwargs={'pk': product.category.pk})

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(*args, **kwargs)


class OrdersListView(ListView):
    model = Order
    template_name = 'adminapp/orders.html'

    def get_context_data(self, **kwargs):
        data = super(OrdersListView, self).get_context_data(**kwargs)
        data['title'] = 'Заказы'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(OrdersListView, self).dispatch(*args, **kwargs)


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'adminapp/order_update.html'
    fields = ('status',)
    success_url = reverse_lazy('adminapp:orders')

    def get_context_data(self, **kwargs):
        data = super(OrderUpdateView, self).get_context_data(**kwargs)
        data['title'] = 'Заказ/Редактирование'
        return data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(OrderUpdateView, self).dispatch(*args, **kwargs)
