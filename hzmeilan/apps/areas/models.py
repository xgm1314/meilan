from django.db import models


# Create your models here.
class Area(models.Model):
    """ 省市区 """
    name = models.CharField(verbose_name='名称', max_length=20, help_text='名称')
    parent = models.ForeignKey(verbose_name='上级行政区', to='self', on_delete=models.SET_NULL,
                               related_name='subs', null=True, blank=True,
                               help_text='上级行政区')  # related_name关联的模型的名字，默认是：关联模型类名的小写_set(area_set),关联自己用to='self'

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
