# _*_coding : uft-8 _*_
# @Time : 2023/7/16 14:43
# @Author : 
# @File : uilt
# @Project : hzmeilan
import re

from django.contrib.auth.backends import ModelBackend
from rest_framework.response import Response

from django.conf import settings

from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData

from . import constants
from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    重构jwt_response_payload_handler方法，使其返回更多数据(源数据只可返回token数据)
    @param token:传入的token数据
    @param user:登录用户数据
    @param request:请求体
    @return:返回token、用户id、用户姓名
    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }


def generic_openid(openid, email):
    """
    数据加密
    @param openid: 传入的token数据进行加密
    @return:返回加密的token数据
    """
    open_serializer = TJWSSerializer(secret_key=settings.SECRET_KEY,
                                     expires_in=constants.TIMED_JSON_WEB_SIGNATURE_SERIALIZER_EXPIRES_IN)
    access_token = open_serializer.dumps({'openid': openid, 'email': email})
    return access_token.decode()


def check_access_token(token):
    """
    数据解密
    @param token: 传入加密后的token数据
    @return: 如果该加密数据存在，则返回，否则返回None
    """
    open_serializer = TJWSSerializer(secret_key=settings.SECRET_KEY,
                                     expires_in=constants.TIMED_JSON_WEB_SIGNATURE_SERIALIZER_EXPIRES_IN)
    try:
        access_token = open_serializer.loads(token)
    except BadData:
        return None
    else:
        return access_token


def get_user_by_account(account):
    """
    传入数据，动态获取user模型对象
    @param account:前端传入的手机号或者用户名
    @return:返回user对象或者None
    """
    try:
        if re.match(r'^1[3-9]\d{9}', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthModelBackend(ModelBackend):
    """ 用户多账号登录 """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
