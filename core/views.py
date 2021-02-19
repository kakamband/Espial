from django.shortcuts import render

def HomeView(request):
    return render(request, 'start.html')
# Create your views here.
