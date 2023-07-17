from django.shortcuts import render

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Area
from .serializers import AreasListModelSerializer, AreasRetrieveModelSerializer


# # Create your views here.
# class AreasListAPIView(ListAPIView):
#     """ 查询所有的省 """
#     queryset = Area.objects.filter(parent=None)
#     serializer_class = AreasListModelSerializer
#
#
# class AreasRetrieveAPIView(RetrieveAPIView):
#     """ 查询所有市区县 """
#     queryset = Area.objects.all()
#     serializer_class = AreasRetrieveModelSerializer


class AreasReadOnlyModelViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """ 查询视图集 """

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AreasListModelSerializer
        else:
            return AreasRetrieveModelSerializer
