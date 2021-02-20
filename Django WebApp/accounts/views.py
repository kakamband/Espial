from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, logout
from .forms import CustomAuthenticationForm
import csv
import json
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from .models import TokenManager

User = get_user_model()

def SignUp(request):
    if request.method == 'POST':
        # f_login = CustomAuthenticationForm()
        if request.POST.get('submit') == 'Login':
            f_login = CustomAuthenticationForm(data=request.POST)
            if f_login.is_valid():
                user = f_login.get_user()
                login(request, user)
                try:
                    url = request.GET['next']
                except:
                    url = 'home'
                return redirect(url)
    else:
        f_login = CustomAuthenticationForm()

    return render(request, 'initsignup.html', {'f_login': f_login})

def Logout(request):
    logout(request)
    return redirect('home')

def ProfileView(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            name = request.POST["name"]
            user = request.user.id
            token = uuid4()
            TokenManager(user=user, name=name, token=token).save()
            return JsonResponse({'status': 200, 'token': token})

        return JsonResponse({'status': 403, 'message': 'Access Denied'})
        
    return render(request, 'profile.html')

# @csrf_exempt
# def getToken(request):
#     if request.method == 'POST':
#         f_login = CustomAuthenticationForm(data=request.POST)
#         if f_login.is_valid():
#             user = f_login.get_user()
#             login(request, user)
#             token = user.token
#             return JsonResponse({'status': 200, 'message': 'Logged In', 'token': token})

#         return JsonResponse({'status': 403, 'message': 'Access Denied'})

#     return JsonResponse({'status': 403, 'message': 'Invalid Request'})
# Create your views here.
