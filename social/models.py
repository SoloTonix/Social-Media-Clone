from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes',  blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def __str__(self):
        return f'{self.author.username}\'s post'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}\'s comment -> {self.post.author}\'s post'
