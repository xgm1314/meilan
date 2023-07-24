# _*_coding : uft-8 _*_
# @Time : 2023/7/23 13:46
# @Author : 
# @File : serializers
# @Project : hzmeilan


from django.utils.datetime_safe import datetime
from django.db import transaction

from django_redis import get_redis_connection

from rest_framework import serializers

from decimal import Decimal

from apps.goods.models import SKU, SPU
from apps.users.models import Address
from .models import OrderInfo, OrderGoods


class CartSKUModelSerializer(serializers.ModelSerializer):
    """ 订单商品序列化器 """
    count = serializers.IntegerField(label='商品购买数量', min_value=1, help_text='商品购买数量')

    class Meta:
        model = SKU
        fields = ['id', 'name', 'default_image', 'price', 'count']


class OrderSettlementSerializer(serializers.Serializer):
    """ 订单序列化器 """
    skus = CartSKUModelSerializer(many=True)
    freight = serializers.DecimalField(label='运费', max_digits=10, decimal_places=2, help_text='运费')


class CommitOrderModelSerializer(serializers.ModelSerializer):
    """ 保存订单序列化器 """

    class Meta:
        model = OrderInfo
        fields = ['order_id', 'address', 'pay_method']
        extra_kwargs = {
            'order_id': {'read_only': True},
            'address': {'write_only': True},
            'pay_method': {'write_only': True}
        }

    def validate(self, attrs):
        user = self.context['request'].user
        user_address = attrs.get('address')
        try:
            address_user = Address.objects.filter(user=user_address.user)
            for address_id in address_user:
                if user.id != address_id.user.id:
                    raise serializers.ValidationError('用户地址错误')
        except Address.DoesNotExist:
            return
        return attrs

    def create(self, validated_data):
        """ 保存订单 """

        # from time import sleep
        # sleep(5)

        user = self.context['request'].user
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%06d' % user.id
        address = validated_data.get('address')
        pay_method = validated_data.get('pay_method')

        if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY']:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']

        with transaction.atomic():
            point = transaction.savepoint()  # 事务开始点

            try:
                orderinfo = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0.00'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=status
                )

                redis_conn = get_redis_connection('cart')
                cart_dict = redis_conn.hgetall('cart_%s' % user.id)
                pipeline = redis_conn.pipeline()
                for sku_id, count in cart_dict.items():
                    for i in range(10):
                        if int(count) > 0:
                            sku = SKU.objects.get(id=sku_id, is_launched=True)

                            cart_sku_count = int(count)

                            old_sku_stock = sku.stock
                            old_sku_sales = sku.sales

                            if cart_sku_count > old_sku_stock:
                                raise serializers.ValidationError('商品库存不足')

                            new_sku_stock = old_sku_stock - cart_sku_count
                            new_sku_sales = old_sku_sales + cart_sku_count

                            # sku.sales = new_sku_sales
                            # sku.stock = new_sku_stock
                            # sku.save()

                            result = SKU.objects.filter(stock=old_sku_stock, id=sku_id).update(stock=new_sku_stock,
                                                                                               sales=new_sku_sales)
                            if result == 0:
                                continue

                            spu = sku.spu
                            spu.sales = spu.sales + new_sku_sales

                            OrderGoods.objects.create(
                                order=orderinfo,
                                sku=sku,
                                count=cart_sku_count,
                                price=sku.price
                            )

                            orderinfo.total_count += cart_sku_count
                            orderinfo.total_amount += (cart_sku_count * sku.price)

                            # pipeline.hdel('cart_%s' % user.id, sku_id)

                            break

                        else:
                            break

                orderinfo.total_amount += orderinfo.freight
                orderinfo.save()
            except Exception:
                transaction.savepoint_rollback(point)  # 事务回滚
                raise serializers.ValidationError('商品数量不足')
            else:
                transaction.savepoint_commit(point)  # 事务提交

        pipeline.execute()
        return orderinfo
