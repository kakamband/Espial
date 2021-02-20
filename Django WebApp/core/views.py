from django.shortcuts import render
from django.http import JsonResponse
from webpush import send_user_notification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from accounts.models import TokenManager
from .models import Document
User = get_user_model()


def HomeView(request):
    return render(request, 'home.html')

def TmpView(request):
    return render(request, 'login.html')

@csrf_exempt
def Notify(request):
    if request.method == "POST":
        try:
            token = request.POST['token']
            vid = request.FILES['video']
            head = None
            head = "Suspicious Activity Detected"
            try:
                cam = TokenManager.objects.get(token=token)
                body = cam.name
                Document(user = cam.user, vid = vid).save()
                obj = Document.objects.filter(user = cam.user).order_by('uploaded_at').last()
                user = User.objects.get(id=cam.user)
                payload = {"head": head, "body": body,
                            "icon": "https://i.imgur.com/dRDxiCQ.png", "url": 'http://127.0.0.1:8000/stream/'+str(obj.vid.url).split('/')[-1]}
                send_user_notification(user=user, payload=payload, ttl=1000)
                return JsonResponse({'status': 200, "message": "Notifier Started"})

            except (User.DoesNotExist, TokenManager.DoesNotExist):
                return JsonResponse({'status': 403, "message": "Access Denied"})
        except:
            return JsonResponse({'status': 403, 'message': 'Forbidden'})

    return JsonResponse({'message': 'You have been judged'})

def Streamer(request, f_name):
    return render(request, 'stream.html', {'vid_url': '/media/documents/'+f_name})
# Create your views here.
