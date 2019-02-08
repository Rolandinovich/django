import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main_view, name='main'),
    path('about/', mainapp.about_view, name='about'),
    path('contact/', mainapp.contact_view, name='contact'),
    path('product_details/<int:pk>/', mainapp.product_details_view, name='product_details'),
    path('products/search/', mainapp.products_search, name='search'),
    path('products/<int:pk>/', mainapp.products_view, name='products'),
    path('products/<str:special>/', mainapp.products_view, name='products'),
    path('get_user_content_ajax/', mainapp.get_user_content_ajax, name='user_content_ajax'),
]
