# _*_coding : uft-8 _*_
# @Time : 2023/7/16 14:43
# @Author : 
# @File : uilt
# @Project : hzmeilan
from rest_framework.response import Response


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
