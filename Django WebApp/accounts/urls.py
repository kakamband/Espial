from django.urls import path
from .views import *

urlpatterns = [
    path('login/', SignUp, name='login'),
    path('token/', getToken, name='get_token'),
    path('logout/', Logout, name='logout'),
]
