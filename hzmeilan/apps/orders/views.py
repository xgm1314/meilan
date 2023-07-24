from django.shortcuts import render
from django_redis import get_redis_connection

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from decimal import Decimal

from apps.goods.models import SKU
from .serializers import OrderSettlementSerializer, CommitOrderModelSerializer


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
