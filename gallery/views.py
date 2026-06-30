from django.shortcuts import render
from django.http import JsonResponse
from gallery.models import Photo
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    photos = Photo.objects.filter(user=request.user).ordered_by('-created_at')
    context = {'photos': photos}
    return render(request, "gallery\index.html", context)

@login_required
def upload_view(request):
    if request.method == "POST":
        files = request.FILES.getlist("images")
        for f in files:
            Photo.objects.create(user=request.user, image=f, file_name=f.name)
        return JsonResponse({"success": True})
