from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout
from .forms import CustomAuthenticationForm
import csv, json

User=get_user_model()

def SignUp(request):
    if request.method == 'POST':
        f_login = CustomAuthenticationForm()

        if request.POST.get('submit') == 'Login':
            f_login = CustomAuthenticationForm(data = request.POST)
            if f_login.is_valid():
                user = f_login.get_user()
                login(request, user)
                try:
                    url = request.GET['next']
                except:
                    url ='home'
                return redirect(url)                
    else:
        f_login = CustomAuthenticationForm()
    
    return render(request, 'initsignup.html', {'f_login': f_login})

def Logout(request):
    logout(request)
    return redirect('home')
    
# Create your views here.
