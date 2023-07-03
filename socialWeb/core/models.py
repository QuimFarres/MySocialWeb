from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime


# Create your models here.
User = get_user_model()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments')

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.now)
    liked_by = models.ManyToManyField(User, related_name='liked_posts')
    comments = models.ManyToManyField(Comment, related_name='post_comments')

    class Meta:
        ordering = ['-created_at']


