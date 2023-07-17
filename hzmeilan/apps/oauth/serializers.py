# _*_coding : uft-8 _*_
# @Time : 2023/7/16 19:59
# @Author : 
# @File : serializers
# @Project : hzmeilan

from django_redis import get_redis_connection

from rest_framework import serializers

from .utlis import check_access_token
from .models import OauthQQUser
from apps.users.models import User


class OauthQQSerializer(serializers.Serializer):
    """ openid绑定用户序列化器 """
    access_token = serializers.CharField(label='openid')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=32, min_length=6)
    sms_code = serializers.CharField(label='验证码', max_length=6)

    def validate(self, attrs):
        # 验证openid
        access_token = attrs.pop('access_token')
        openid = check_access_token(access_token)
        if openid is None:
            raise serializers.ValidationError('openid已过期')
        attrs['openid'] = openid
        # 验证验证码
        redis_conn = get_redis_connection('sms_code')
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')
        sms_code_redis = redis_conn.get('sms_%s' % mobile)
        if (sms_code_redis is None) or (sms_code_redis.decode() != sms_code):
            raise serializers.ValidationError('验证码错误')
        # 验证手机号
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create(
                username='ML_%s' % attrs['mobile'],
                mobile=attrs['mobile']
            )
            user.set_password(attrs['password'])
            user.save()

        if user.check_password(attrs['password']) is False:
            raise serializers.ValidationError('用户名或者手机号不正确')
        else:
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        openid = validated_data.get('openid')
        OauthQQUser.objects.create(
            user=user,
            openid=openid
        )
        return user
