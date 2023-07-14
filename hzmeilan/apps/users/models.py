from django.db import models
import django.contrib.auth.models


# Create your models here.
class User(django.contrib.auth.models.AbstractUser):
    """ 用户表 """
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True, help_text='手机号')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
