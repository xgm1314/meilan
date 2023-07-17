from django.db import models

from utils.models import BaseModels
from apps.users.models import User


# Create your models here.
class OauthQQUser(BaseModels):
    """ QQ登录 """
    user = models.ForeignKey(verbose_name='用户', to=User, on_delete=models.CASCADE)
    openid = models.CharField(verbose_name='openid', max_length=64, db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'qq登录表'
        verbose_name_plural = verbose_name
