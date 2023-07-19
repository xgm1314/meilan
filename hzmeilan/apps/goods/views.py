from django.shortcuts import render

from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from .models import SKU, GoodsCategory
from .serializers import SKUModelSerializer, CategoryModelSerializer


# Create your views here.
class SKUGenericAPIView(GenericAPIView):
    """ 商品列表查询 """
    filter_backends = [OrderingFilter]
    ordering_filter = ['create_time', 'price', 'sales']
    serializer_class = SKUModelSerializer

    def get_queryset(self, pk=None):
        return SKU.objects.filter(is_launched=True, category_id=pk)

    def get(self, request, pk=None):
        """
        商品列表序列化查询
        @param request:请求体
        @param pk:商品类别
        @return:
        """
        sku_category = self.filter_queryset(self.get_queryset(pk=pk))  # 获取过滤后的排序数据
        serializer = self.get_serializer(instance=sku_category, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response


class CategoryGenericAPIView(GenericAPIView):
    """ 商品面包屑展示 """
    queryset = GoodsCategory.objects.all()
    serializer_class = CategoryModelSerializer

    def get(self, request, pk=None):
        """
        商品类别面包屑展示
        @param request: 请求头
        @param pk: 商品类别
        @return:返回面包屑字典
        """
        ret = {
            'cat1': '',
            'cat2': '',
            'cat3': ''
        }
        queryset = self.get_object()
        if queryset.parent is None:
            ret['cat1'] = self.get_serializer(queryset).data
        elif queryset.subs.count() == 0:
            ret['cat3'] = self.get_serializer(queryset).data
            ret['cat2'] = self.get_serializer(queryset.parent).data
            ret['cat1'] = self.get_serializer(queryset.parent.parent).data
        else:
            ret['cat2'] = self.get_serializer(queryset).data
            ret['cat1'] = self.get_serializer(queryset.parent).data
        return Response(ret)
