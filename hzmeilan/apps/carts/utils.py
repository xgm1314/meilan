# _*_coding : uft-8 _*_
# @Time : 2023/7/22 13:37
# @Author : 
# @File : utils
# @Project : hzmeilan

import base64
import pickle

from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """
    将cookie中的购物车数据添加到redis中
    @param request: 传入的请求体
    @param user: 传入的用户模型
    @param response: 响应体,用来删除cookie数据
    @return: 返回响应体
    """
    cart_str = request.COOKIES.get('cart')
    if cart_str is None:
        return

    cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
    redis_conn = get_redis_connection('cart')
    # cart_dict={1:{count:1,selected:true}}
    for sku_id, count_selected in cart_dict.items():
        count = count_selected.get('count')
        selected = count_selected.get('selected')

        redis_cart = redis_conn.hgetall('cart_%s' % user.id)
        for redis_sku_key, redis_sku_value in redis_cart.items():
            if (sku_id == int(redis_sku_key)) and (int(redis_sku_value) > 0):
                selected_cart = True
            else:
                selected_cart = False
            break

        if selected or selected_cart:
            redis_conn.hset('cart_%s' % user.id, sku_id, count)
        else:
            redis_conn.hset('cart_%s' % user.id, sku_id, -count)

    response.delete_cookie('cart')
    return response
