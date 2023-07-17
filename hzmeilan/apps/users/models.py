from django.db import models
import django.contrib.auth.models
from django.conf import settings

from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData

from utils.models import BaseModels


# Create your models here.
class User(django.contrib.auth.models.AbstractUser):
    """ 用户表 """
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True, help_text='手机号')
    email_active = models.BooleanField(verbose_name='邮箱激活状态', default=False, help_text='邮箱激活状态')
    default_address = models.ForeignKey(to='Address', related_name='users', on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name='默认地址', help_text='默认地址')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def generate_email_verify_url(self):
        """ 生成token_id """
        serializer = TJSSerializer(secret_key=settings.SECRET_KEY, expires_in=60 * 60 * 24)
        data = {'user_id': self.id, 'email': self.email}
        token_id = serializer.dumps(data).decode()
        return token_id

    @staticmethod  # 调用静态方法
    def check_verify_email_token(token):
        """ 解密数据 """
        serializer = TJSSerializer(secret_key=settings.SECRET_KEY, expires_in=60 * 60 * 24)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=id, email=email)
        except User.DoesNotExist:
            return None
        return user


class Address(BaseModels):
    """ 用户收货地址 """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户',
                             help_text='用户')
    title = models.CharField(verbose_name='地址名称', max_length=20, help_text='地址名称')
    receiver = models.CharField(verbose_name='收货人', max_length=20, help_text='收货人')
    province = models.ForeignKey('areas.Area', verbose_name='省', on_delete=models.PROTECT,
                                 related_name='province_addresses', help_text='省')
    city = models.ForeignKey('areas.Area', verbose_name='市', on_delete=models.PROTECT, related_name='city_addresses',
                             help_text='市')
    district = models.ForeignKey('areas.Area', verbose_name='区', on_delete=models.PROTECT,
                                 related_name='district_addresses', help_text='区县')
    place = models.CharField(verbose_name='详细地址', max_length=50, help_text='详细地址')
    mobile = models.CharField(verbose_name='手机号', max_length=11, help_text='手机号')
    tel = models.CharField(verbose_name='固定电话', max_length=20, null=True, blank=True, default='', help_text='固定电话')
    email = models.CharField(verbose_name='邮箱', max_length=30, null=True, blank=True, default='', help_text='邮箱')
    is_deleted = models.BooleanField(verbose_name='逻辑删除', default=False, help_text='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']
