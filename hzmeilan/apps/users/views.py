from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserCreateModelSerializer, UserRetrieveModelSerializer
from .models import User


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """ 用户注册 """
    serializer_class = UserCreateModelSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """ 用户详情页面 """
    queryset = User.objects.all()
    serializer_class = UserRetrieveModelSerializer
    permission_classes = [IsAuthenticated]

