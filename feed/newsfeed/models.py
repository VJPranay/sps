from django.contrib.gis.db import models
from feed.users.models import User
# Create your models here.


class Activity(models.Model):
    post_types = [
        ('FR','Friends'),
        ('NB','NearBy'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='users')
    datetime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    post_type = models.CharField(max_length=255,blank=True,null=True,choices=post_types)
    image = models.ImageField(blank=True,null=True)
    video = models.FileField(blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    location = models.PointField(blank=True,null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=None, blank=True, null=True)
    post = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=None, blank=True, null=True)
    post = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)



