from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField


# Create your models here.
class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')

    # main info
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    # file data
    file_name = models.CharField(max_length=200)
    file_size = models.PositiveIntegerField(default=0) # bytes
    resolution = models.CharField(max_length=50)
    megapixels = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    # EXIF data
    date_taken = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(max_length=50, null=True, blank=True)
    camera_model = models.CharField(max_length=100, null=True, blank=True)
    exposure_time = models.CharField(max_length=50, null=True, blank=True)
    iso = models.IntegerField(null=True, blank=True)
    lense_model = models.CharField(max_length=100, null=True, blank=True)
    aperture = models.CharField(max_length=20, null=True, blank=True)
    focal_length = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
