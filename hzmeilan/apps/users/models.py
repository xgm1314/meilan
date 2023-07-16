from django.db import models
import django.contrib.auth.models
from django.conf import settings

from itsdangerous import TimedJSONWebSignatureSerializer as TJSSerializer, BadData


# Create your models here.
class User(django.contrib.auth.models.AbstractUser):
    """ 用户表 """
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True, help_text='手机号')
    email_active = models.BooleanField(verbose_name='邮箱激活状态', default=False, help_text='邮箱激活状态')

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
