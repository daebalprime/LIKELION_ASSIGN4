from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(gender=self.model.GENDER_OTHER, *args, **kwargs)


class User(AbstractUser):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    CHOICES_GENDER = (
        (GENDER_MALE, '남성'),
        (GENDER_FEMALE, '여성'),
        (GENDER_OTHER, '기타'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    like_posts = models.ManyToManyField('post.Post', blank=True, related_name='like_users')

    hate_foods = models.ManyToManyField('post.Food', blank=True, related_name='hate_foods')
    like_foods = models.ManyToManyField('post.Food', blank=True, related_name='like_foods')

    objects = UserManager()

    def __str__(self):
        return self.username
