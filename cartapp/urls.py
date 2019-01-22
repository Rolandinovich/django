import cartapp.views as cartapp
from django.urls import path

app_name = 'cartapp'

urlpatterns = [
    path('', cartapp.CartListView.as_view(), name='view'),
    # path('', cartapp.cart_ajax, name='view'),
    path('add/<int:pk>/<int:add_quantity>/', cartapp.cart_add, name='add'),
    path('add/<int:pk>/', cartapp.cart_add, name='add'),
    path('remove/<int:pk>/', cartapp.cart_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', cartapp.cart_edit, name='edit'),
]
