from django.urls import path
from .views import *

urlpatterns = [
    path('login/', SignUp, name='login'),
    path('logout/', Logout, name='logout'),
]
