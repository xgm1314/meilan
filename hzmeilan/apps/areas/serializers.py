# _*_coding : uft-8 _*_
# @Time : 2023/7/17 10:24
# @Author : 
# @File : serializers
# @Project : hzmeilan

from rest_framework import serializers

from .models import Area


class AreasListModelSerializer(serializers.ModelSerializer):
    """ 查询省序列化器 """

    class Meta:
        model = Area
        fields = ['id', 'name']


class AreasRetrieveModelSerializer(serializers.ModelSerializer):
    """ 查询市区县序列化器 """
    subs = AreasListModelSerializer(many=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
