# _*_coding : uft-8 _*_
# @Time : 2023/7/16 17:37
# @Author : 
# @File : utlis
# @Project : hzmeilan

from django.conf import settings

from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData

from apps.oauth import constants


def generic_openid(openid):
    """
    数据加密
    @param openid: 传入的token数据进行加密
    @return:返回加密的token数据
    """
    open_serializer = TJWSSerializer(secret_key=settings.SECRET_KEY,
                                     expires_in=constants.TIMED_JSON_WEB_SIGNATURE_SERIALIZER_EXPIRES_IN)
    access_token = open_serializer.dumps({'openid': openid})
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
        return access_token.get('openid')
