# _*_coding : uft-8 _*_
# @Time : 2023/7/19 8:53
# @Author : 
# @File : serializers
# @Project : hzmeilan

from rest_framework import serializers

from .models import SKU, GoodsCategory


class SKUModelSerializer(serializers.ModelSerializer):
    """ 商品列表查询序列化器 """

    class Meta:
        model = SKU
        fields = ['id', 'name', 'price', 'sales', 'update_time', 'comments', 'default_image']


class CategoryModelSerializer(serializers.ModelSerializer):
    """ 商品类别面包屑展示 """

    class Meta:
        model = GoodsCategory
        fields = ['name']
