from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.decorators import action

from . import constants
from .serializers import UserCreateModelSerializer, UserRetrieveModelSerializer, EmailUpdateModelSerializer, \
    AddressGenericModelSerializer, TitleModelSerializer
from .models import User, Address
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


class AddressGenericViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ 用户地址的增删改查 """
    serializer_class = AddressGenericModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def list(self, request):
        """ 用户地址展示 """
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        user = self.request.user
        response = Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'address': serializer.data,
            'limit': constants.ADDRESS_LIMIT
        }, status=status.HTTP_200_OK)
        return response

    def create(self, request):
        """ 用户新增地址 """
        user = request.user
        count = Address.objects.filter(user=user, is_deleted=False).count()
        if count >= constants.ADDRESS_LIMIT:
            return Response({'message': '收货地址数量达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
        else:
            return Response({'message': '添加失败'}, status=status.HTTP_400_BAD_REQUEST)
        if count == 0:
            user = User.objects.get(id=request.user.id)
            user.default_address_id = data.id
            user.save()
        response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response

    def destroy(self, request, pk=None):
        """ 逻辑删除地址 """
        address = self.get_object()
        address.is_deleted = True
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None):
        """ 修改标题 """
        address = self.get_object()
        serializer = TitleModelSerializer(instance=address, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({'message': '修改失败，请重试'})
        response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return response

    @action(methods=['put'], detail=True)
    def status(self, request, pk=None):
        """ 修改默认地址 """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        response = Response({'message': 'ok'}, status=status.HTTP_201_CREATED)
        return response
