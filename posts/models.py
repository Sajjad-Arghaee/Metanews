import uuid
from django.db import models
from users.models import Profile


class Post(models.Model):
    topic = models.CharField(max_length=25, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts/', default='posts/default.jpg')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    views_count = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-views_count']

    def __str__(self):
        return self.title
