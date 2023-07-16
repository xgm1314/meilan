from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserCreateModelSerializer, UserRetrieveModelSerializer, EmailUpdateModelSerializer
from .models import User
from .utils import check_access_token


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """ 用户注册 """
    serializer_class = UserCreateModelSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """ 用户详情页面 """
    queryset = User.objects.all()
    serializer_class = UserRetrieveModelSerializer
    permission_classes = [IsAuthenticated]


class EmailUpdateAPIView(UpdateAPIView):
    """ 修改邮箱 """
    queryset = User.objects.all()
    serializer_class = EmailUpdateModelSerializer
    permission_classes = [IsAuthenticated]


class EmailActivationAPIView(APIView):
    """ 激活用户邮箱 """

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '激活链接已过期'}, status=status.HTTP_400_BAD_REQUEST)

        # 方式一：
        # user = User.check_verify_email_token(token)

        # 方式二：
        access_token = check_access_token(token)
        openid = access_token.get('openid')
        email = access_token.get('email')
        try:
            user = User.objects.get(id=openid, email=email)
        except User.DoesNotExist:
            return None

        if user is None:
            return Response({'message': '激活失败'}, status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()
        return Response({'message': 'ok'})
