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
            token = request.POST['token']
            try:
                user = User.objects.get(token = token)
            
            except User.DoesNotExist:
                return JsonResponse({'status': 403, "message": "Access Denied"})
            
            head = request.POST['head']
            body = request.POST['body']
            payload = {"head": head, "body": body, "icon": "https://i.imgur.com/dRDxiCQ.png", "url": "https://www.example.com"}
            send_user_notification(user=user, payload=payload, ttl=1000)
            return JsonResponse({'status': 200, "message": "Notifier Started"})

        except:
            return JsonResponse({'status':403, 'message': 'Forbidden'})

    return JsonResponse({'message': 'You have been judged'})

# Create your views here.
