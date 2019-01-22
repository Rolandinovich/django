import wishapp.views as wishapp
from django.urls import path

app_name = 'wishapp'

urlpatterns = [
    path('', wishapp.WishListView.as_view(), name='view'),
    #path('', wishapp.wish, name='view'),
    path('add/<int:pk>/', wishapp.wish_add, name='add'),
    path('remove/<int:pk>/', wishapp.wish_remove, name='remove'),
]
