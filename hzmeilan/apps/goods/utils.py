# _*_coding : uft-8 _*_
# @Time : 2023/7/18 19:54
# @Author : 
# @File : utils
# @Project : hzmeilan
import time
import os

from django.template import loader
from django.conf import settings

from collections import OrderedDict

from apps.goods.models import GoodsChannel


def get_categories():
    """
    获取商城商品分类菜单
    @return: 分类菜单字典
    """

    # 商品首页组分类
    categories = OrderedDict()  # 创建有序字典
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组
        if group_id not in categories:
            categories[group_id] = {'channel': [], 'sequence': []}
        cat1 = channel.category  # 当前组频道的分类
        categories[group_id]['channel'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        for cat2 in cat1.goodschannel_set.all():
            categories[group_id]['sequence'].append(cat2)

    return categories
