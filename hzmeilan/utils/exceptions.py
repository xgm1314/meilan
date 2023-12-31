# _*_coding : uft-8 _*_
# @Time : 2023/6/13 17:06
# @Author : 
# @File : exceptions
# @Project : meiduo_drf
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.db import DatabaseError
from redis.exceptions import RedisError

import logging

logger = logging.getLogger('django')  # 获取在配置文件中定义的logger，用来记录日志


def exception_handler(exc, context):
    """
    自定义异常处理
    @param exc: 异常实例对象
    @param context: 抛出异常的上下文(包含request和view对象)
    @return: Response响应对象
    """
    # 调用drf框架原生的异常处理方法
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context['view']
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s]%s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
