# _*_coding : uft-8 _*_
# @Time : 2023/6/20 10:51
# @Author : 
# @File : models
# @Project : meiduo_drf
from django.db import models


class BaseModels(models.Model):
    """ 定义基类 补充时间字段 """
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        abstract = True  # 说明是抽象模型类，只做继承用
