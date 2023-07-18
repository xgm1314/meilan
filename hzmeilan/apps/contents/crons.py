# _*_coding : uft-8 _*_
# @Time : 2023/7/17 19:32
# @Author : 
# @File : crons
# @Project : hzmeilan
import time
import os

from django.template import loader
from django.conf import settings

from collections import OrderedDict

from apps.goods.models import GoodsChannel
from .models import ContentCategory


def generate_static_index_html():
    """ 生成静态的主页HTML文件 """
    print('%s:generate_static_index_html' % time.ctime())

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

    # 广告分类
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    content = {
        'categories': categories,  # 商品频道组数据
        'contents': contents  # 广告组数据
    }

    template = loader.get_template('index.html')  # 加载模板文件
    html_text = template.render(content)  # 渲染模板
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
