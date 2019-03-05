from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='post')
    text = models.TextField(default='')
    title = models.CharField(max_length=64, default="")

    def __str__(self):
        return f'Post (PK: {self.pk}, Author: {self.author.username})'



class Provider(models.Model):
    name = models.CharField(max_length=31)
    logo = models.ImageField(upload_to="post")
    score = models.IntegerField(default="50")
    toxic = models.IntegerField(default="50")

    def __str__(self):
        return f'Provider ({self.pk}: {self.name})'

class Food(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='foodprovider', default=9999)
    photo = models.ImageField(upload_to='post')
    name = models.CharField(default='', max_length=63)
    toxic = models.IntegerField(default="50")
    score = models.IntegerField(default="50")
    price = models.IntegerField(default=0)

    def __str__(self):
        return f'Food ({self.provider}{self.pk}: {self.name})'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='comments', blank=True, null=True)
    food = models.ForeignKey(Food, on_delete=models.PROTECT, related_name='comments_food', blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name='comments_provider', blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE) ## Settings에 정의해준 상수?
    content = models.TextField(default='')

    def __str__(self):
        return f'Comment (PK: {self.pk}, Author: {self.author.username})'
