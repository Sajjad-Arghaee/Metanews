from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    short_intro = models.CharField(max_length=250, null=True, blank=True)
    full_intro = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True, max_length=250)
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/profiles/',
                                      default='images/profiles/default.png')
    active_posts = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    subject = models.CharField(max_length=500, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject if self.subject is not None else 'None'

    class Meta:
        ordering = ['seen', '-created']
