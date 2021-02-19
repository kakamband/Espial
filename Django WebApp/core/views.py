from django.shortcuts import render
from django.http import HttpResponse
from webpush import send_user_notification

def HomeView(request):
    return render(request, 'start.html')

def Notify(request):
    payload = {"head": "Aa hi gaye aap", "body": "Hello World", "icon": "https://i.imgur.com/dRDxiCQ.png", "url": "https://www.example.com"}
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    return HttpResponse("Notification Pushed !!")

# Create your views here.
