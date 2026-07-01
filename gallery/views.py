from django.core.handlers.exception import response_for_exception
from django.shortcuts import render
from django.http import JsonResponse
from gallery.models import Photo
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@login_required
def index(request):
    photos = Photo.objects.filter(user=request.user).order_by('-created_at')
    context = {'photos': photos}
    return render(request, "gallery/index.html", context)

@login_required
def upload_view(request):
    if request.method == "POST":
        files = request.FILES.getlist("images")
        for f in files:
            Photo.objects.create(user=request.user, image=f, file_name=f.name)
        return JsonResponse({"success": True})

@csrf_exempt
def auth_view(request):
    print(f"DEBUG: Request method is {request.method}")  # Увидите в консоли терминала
    print(f"DEBUG: Request path is {request.path}")

    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")
        username = data.get("username")
        password = data.get("password")
        print(username, password)

        if action == "login":
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"status": "ok"})
            return JsonResponse({'status': 'error', 'message': 'Неверный логин или пароль'}, status=400)
        elif action == "register":
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return JsonResponse({"status": "ok"})
            return JsonResponse({'status': 'error', 'message': 'Пользователь уже существует'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Метод не поддерживается'}, status=405)

def auth(request):
    return render(request, "gallery/auth.html")
