from django.shortcuts import render
from django.http import JsonResponse
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()

def HomeView(request):
    return render(request, 'start.html')

@csrf_exempt
def Notify(request):
    if request.method == "POST":
        try:
            user = request.POST['user']
            user = User.objects.get(email = user)
            head = request.POST['head']
            body = request.POST['body']
        except:
            user = request.user
            head = "Aur Janab"
            body = "Yo"

        payload = {"head": head, "body": body, "icon": "https://i.imgur.com/dRDxiCQ.png", "url": "https://www.example.com"}
        send_user_notification(user=user, payload=payload, ttl=1000)
        return JsonResponse(payload)

    return JsonResponse({'message': 'You have been judged'})

# Create your views here.
