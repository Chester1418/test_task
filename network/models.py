from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)
    unlike = models.IntegerField(default=0)

    def __str__(self):
        return f'<Post {self.title[:30]}>'
