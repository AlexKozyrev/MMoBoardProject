from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class AdCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    dateCreation = models.DateTimeField(auto_now_add=True)
    content = RichTextField()

    def preview(self):
        return self.content[0:123] + '...'

    def __str__(self):
        return f'{self.title}: {self.preview()[:20]}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    accepted = models.BooleanField(default=False)

    def preview(self):
        return self.content[0:123] + '...'

    def __str__(self):
        return f'{self.preview()[:20]}'