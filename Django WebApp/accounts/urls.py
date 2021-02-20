from django.urls import path
from .views import *

urlpatterns = [
    path('login/', SignUp, name='login'),
    # path('token/', GenerateToken, name='get_token'),
    path('logout/', Logout, name='logout'),
    path('profile/', ProfileView, name='profile'),

]
