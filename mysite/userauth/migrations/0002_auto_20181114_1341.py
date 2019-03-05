# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-14 13:41
from __future__ import unicode_literals

from django.db import migrations, models
import userauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_title'),
        ('userauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', userauth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('m', '남성'), ('f', '여성'), ('o', '기타')], default='o', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='user'),
        ),
        migrations.AddField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(blank=True, related_name='like_users', to='post.Post'),
        ),
    ]
