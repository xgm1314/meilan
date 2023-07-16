# _*_coding : uft-8 _*_
# @Time : 2023/7/14 10:41
# @Author : 
# @File : serializers
# @Project : hzmeilan

import re

from rest_framework import serializers

from django_redis import get_redis_connection

from .models import User


class UserCreateModelSerializer(serializers.ModelSerializer):
    """ 注册用户序列化器 """
    password2 = serializers.CharField(label='确认密码', max_length=32, min_length=6, write_only=True)
    sms_code = serializers.CharField(label='验证码', max_length=6, min_length=4, write_only=True)
    allow = serializers.BooleanField(label='是否同意用户协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'password', 'password2', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 2,
                'max_length': 20,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '用户名字不能少于2个字符',
                    'max_length': '用户名字不能大余20个字符',
                }
            },
            'password': {
                'min_length': 6,
                'max_length': 32,
                "write_only": True,
                'error_messages': {  # 自定义校验出错后的错误信息提示
                    'min_length': '密码不能少于6个字符',
                    'max_length': '密码不能大余32个字符',
                }
            },
        }

    def validate(self, attrs):

        username = attrs.get('username')
        mobile = attrs.get('mobile')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        allow = attrs.get('allow')
        sms_code = attrs.get('sms_code')

        if not username.isalpha():
            return serializers.ValidationError('用户名应以字母开头')
        if not re.match('1[345789]\d{9}', mobile):
            return serializers.ValidationError('手机号格式不正确')
        if password != password2:
            return serializers.ValidationError('两次密码不一致')
        if allow != True:
            return serializers.ValidationError('请同意用户协议')

        redis_conn = get_redis_connection('sms_code')
        code_redis = redis_conn.get('sms_%s' % mobile)
        if code_redis is None or sms_code != code_redis.decode():
            return serializers.ValidationError('验证码有误')
        return attrs

    def create(self, validated_data):
        # ['id', 'username', 'mobile', 'password', 'password2', 'sms_code', 'allow', 'token']
        # 保存重写
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # 生成token数据
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER  # 手动创建新令牌
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER  # 手动创建新令牌
        # 生成载荷信息(payload),根据user的信息生成一个payload
        payload = jwt_payload_handler(user)
        # 根据payload和secret_key，采用HS256，生成token.
        token = jwt_encode_handler(payload)
        # print(token)
        # 将token信息传递给用户信息
        user.token = token

        return user


class UserRetrieveModelSerializer(serializers.ModelSerializer):
    """ 用户详情页面序列化器 """

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']
        extra_kwargs = {
            'email': {
                'required': True
            }
        }
