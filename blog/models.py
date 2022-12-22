from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images')
    @property
    def isoformat(self):
        if self.published_date:
            return self.published_date.strftime("%H:%M:%S %b %d %Y")
        return ''

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title