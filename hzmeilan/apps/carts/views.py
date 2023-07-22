import base64
import pickle

from django.shortcuts import render

from django_redis import get_redis_connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CartsSerializer, SKUCartsModelSerializer, CartDeleteSerializer, CartSelectedAllSerializer
from apps.goods.models import SKU


# Create your views here.

class CartsAPIView(APIView):
    """ 购物车增删改查 """

    def post(self, request):
        """
        购物车新增
        @param request:请求体
        @return: 返回添加对象
        """
        """
        测试数据
        {
        "sku_id": 1,
        "count":2,
        "selected":"False"
        }
        """
        serializer = CartsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sku_id = serializer.validated_data.get('sku_id')
            # count>0代表勾选,count<0代表未勾选,abs求绝对值
            count = serializer.validated_data.get('count')
            selected = serializer.validated_data.get('selected')
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '商品信息错误'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')

            if selected:

                if redis_conn.hget('cart_%s' % user.id, sku_id) is None:
                    redis_conn.hset('cart_%s' % user.id, sku_id, count)
                else:
                    if int(redis_conn.hget('cart_%s' % user.id, sku_id)) > 0:
                        redis_conn.hincrby('cart_%s' % user.id, sku_id, count)
                    else:
                        count = abs(int(redis_conn.hget('cart_%s' % user.id, sku_id))) + count
                        redis_conn.hset('cart_%s' % user.id, sku_id, count)

            else:
                if redis_conn.hget('cart_%s' % user.id, sku_id) is None:
                    redis_conn.hset('cart_%s' % user.id, sku_id, -count)
                else:
                    if int(redis_conn.hget('cart_%s' % user.id, sku_id)) > 0:
                        count = -int(redis_conn.hget('cart_%s' % user.id, sku_id)) - count
                        redis_conn.hset('cart_%s' % user.id, sku_id, count)
                    elif int(redis_conn.hget('cart_%s' % user.id, sku_id)) < 0:
                        count = int(redis_conn.hget('cart_%s' % user.id, sku_id)) - count
                        redis_conn.hset('cart_%s' % user.id, sku_id, count)

        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            if sku_id in cart_dict:
                old_count = cart_dict[sku_id]['count']
                count += old_count

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('cart', cart_str, expires=3600 * 24)
        return response

    def get(self, request):
        """
        查询购物车
        @param request:请求体
        @return: 返回购物车的对象
        """
        user = request.user

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            cart_redis_dict = redis_conn.hgetall('cart_%s' % user.id)
            cart_dict = {}
            for sku_id_byes, count_byes in cart_redis_dict.items():
                cart_dict[int(sku_id_byes)] = {
                    'count': abs(int(count_byes)),
                    'selected': int(count_byes) > 0
                }
        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return Response({'message': '购物车数据不存在'}, status=status.HTTP_400_BAD_REQUEST)

        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            sku.count = cart_dict[sku.id]['count']
            sku.selected = cart_dict[sku.id]['selected']
        serializer = SKUCartsModelSerializer(instance=skus, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response

    def put(self, request):
        """
        修改购物车
        @param request: 请求体
        @return: 返回修改的对象
        """
        serializer = CartsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            sku_id = serializer.validated_data.get('sku_id')
            # count>0代表勾选,count<0代表未勾选
            count = serializer.validated_data.get('count')
            selected = serializer.validated_data.get('selected')
            response = Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '商品信息错误'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            if selected:
                redis_conn.hset('cart_%s' % user.id, sku_id, count)
            else:
                redis_conn.hset('cart_%s' % user.id, sku_id, -count)
        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return Response({'message': '购物车信息不存在'})

            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }

            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('cart', cart_str, expires=3600 * 24)

        return response

    def delete(self, request):
        """
        删除购物车数据
        @param request: 请求体
        @return:
        """
        serializer = CartDeleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sku_id = serializer.validated_data.get('sku_id')
        else:
            return Response({'message': '购物车商品信息不存在'})
        # sku_id=16 # 测试
        response = Response(status=status.HTTP_204_NO_CONTENT)

        user = request.user

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_conn.hdel('cart_%s' % user.id, sku_id)
        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return Response({'message': '购物车信息不存在'})

            if sku_id in cart_dict:
                del cart_dict[sku_id]

            if len(cart_dict.keys()):
                cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
                response.set_cookie('cart', cart_str, expires=3600 * 24)
            else:
                response.delete_cookie('cart')

        return response


class CartSelectedAllAPIView(APIView):
    """ 购物车全选 """

    def put(self, request):
        """
        修改购物车全选
        @param request: 请求体
        @return:
        """
        """
        测试数据
        {
        "selected":"true"
        }
        """
        serializer = CartSelectedAllSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            selected = serializer.validated_data.get('selected')
        else:
            return Response({'message': '购物车信息不存在'})

        response = Response(data=serializer.data, status=status.HTTP_200_OK)

        user = request.user

        if user and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            cart_dict_redis = redis_conn.hgetall('cart_%s' % user.id)
            # sku_ids = cart_dict_redis.keys()

            for sku_id_byes, count_byes in cart_dict_redis.items():
                if selected:
                    redis_conn.hset('cart_%s' % user.id, int(sku_id_byes), abs(int(count_byes)))
                else:
                    redis_conn.hset('cart_%s' % user.id, int(sku_id_byes), -abs(int(count_byes)))

        else:
            cart_str = request.COOKIES.get('cart')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                return Response({'message': '购物车信息不存在'})

            for sku_id in cart_dict:
                cart_dict[sku_id]['selected'] = selected

            cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
            response.set_cookie('cart', cart_str, expires=3600 * 24)
        return response
