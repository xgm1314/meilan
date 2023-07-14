from django.shortcuts import render

from rest_framework.generics import CreateAPIView

from .serializers import UserModelSerializer


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """ 用户注册 """
    serializer_class = UserModelSerializer
