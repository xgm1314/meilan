from django.shortcuts import render
from django_redis import get_redis_connection

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView

from decimal import Decimal

from apps.goods.models import SKU
from .serializers import OrderSettlementSerializer, CommitOrderModelSerializer, OrderInfoModelSerializer, \
    OrderInfoDeleteModelSerializer, CancellationOrderModelSerializer
from .models import OrderInfo, OrderGoods


# Create your views here.

class OrderSettlementAPIView(APIView):
    """ 去结算 """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        查询redis库,选择勾选的商品取结算
        @param request:请求体
        @return:要结算的商品
        """
        user = request.user
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        skus = []
        for sku_id, count in redis_cart.items():
            if int(count) > 0:
                try:
                    sku = SKU.objects.get(id=sku_id, is_launched=True)
                except SKU.DoesNotExist:
                    return Response({'message': '商品信息不存在'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    sku.count = int(count)
                    skus.append(sku)
        freight = Decimal('10.00')  # 运费
        data_dict = {'freight': freight, 'skus': skus}
        serializer = OrderSettlementSerializer(instance=data_dict)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response


class CommitOrderCreateAPIView(CreateAPIView):
    """ 去结算, 新增订单 """
    permission_classes = [IsAuthenticated]
    serializer_class = CommitOrderModelSerializer
    queryset = ''

    # def get_queryset(self):
    #     return self.request.user.addresses.filter(is_deleted=False)


class OrderListAPIView(APIView):
    """ 查看订单 """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = OrderInfo.objects.filter(user=user, is_deleted=False)
        serializer = OrderInfoModelSerializer(instance=data, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response


class OrderDestroyAPIView(APIView):
    """ 删除订单(逻辑删除) """
    permission_classes = [IsAuthenticated]

    """
    测试数据
    {"order_id":"20230723161916000001","is_deleted":"true"}
    """

    def put(self, request, pk=None):
        user = request.user
        queryset = request.data
        try:
            data = OrderInfo.objects.get(user=user, order_id=pk, is_deleted=False)
        except OrderInfo.DoesNotExist:
            return Response({'message': '该订单不存在'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderInfoDeleteModelSerializer(instance=data, data=queryset)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({'message': '删除错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CancellationOrderUpdateAPIView(APIView):
    """ 取消订单 """
    permission_classes = [IsAuthenticated]

    # serializer_class = CancellationOrderModelSerializer

    def put(self, request):
        user = request.user
        order_id = request.data['order_id']
        try:
            queryset = OrderInfo.objects.get(user=user, order_id=order_id, is_deleted=False)
        except OrderInfo.DoesNotExist:
            return Response({'message': '订单异常'}, status=status.HTTP_404_NOT_FOUND)

        # goods = OrderGoods.objects.filter(order_id=queryset)
        #
        # for good in goods:
        #     sku = SKU.objects.get(id=good.id)
        #     order_count = good.count
        #
        #     sku.stock += order_count
        #     sku.sales -= order_count
        #     sku.save()
        #
        #     spu = sku.spu
        #     spu.sales -= order_count
        #     spu.save()
        #
        # OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['CANCELED'])

        serializer = CancellationOrderModelSerializer(instance=queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({'message': '订单取消失败'})

        return Response({'message': '订单取消成功'})
