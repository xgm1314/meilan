# _*_coding : uft-8 _*_
# @Time : 2023/7/18 19:58
# @Author : 
# @File : tasks
# @Project : hzmeilan

import os

from celery_tasks.main import celery_app

from django.template import loader
from django.conf import settings

from apps.goods.utils import get_categories


@celery_app.task(name='generate_static_list_search_html')
def generate_static_list_search_html():
    """ 生成静态文件的商品列表和搜索结果页面的html文件 """
    categories = get_categories()  # 调用商品分类的菜单
    context = {  # 渲染模板
        'categories': categories
    }
    template = loader.get_template('list.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'list.html')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
