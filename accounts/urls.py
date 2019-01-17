
import accounts.views as accounts
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', accounts.login, name='login'),
    path('logout/', accounts.logout, name='logout'),
    path('register/', accounts.register, name='register'),
    path('edit/', accounts.edit, name='edit'),
    path('verify/<str:email>/<str:activation_key>/', accounts.verify, name='verify'),

]