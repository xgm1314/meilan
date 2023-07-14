import logging

from django.shortcuts import render
from django_redis import get_redis_connection

from random import randint

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import constants
from libs.yuntongxun.sms import CCP
from celery_tasks.sms.tasks import send_sms_code

logger = logging.getLogger('django')


# Create your views here.
class SMSCodeAPIView(APIView):
    """ 短信验证码 """

    def get(self, request, mobile):
        redis_conn = get_redis_connection('sms_code')

        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({'message': '短信验证码发送过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        sms_code = '%04d' % randint(0, 9999)

        logger.info(sms_code)

        pipeline = redis_conn.pipeline()
        pipeline.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pipeline.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pipeline.execute()

        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], 1)  # 调用函数，发送短信

        send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'ok'})
