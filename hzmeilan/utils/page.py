# _*_coding : uft-8 _*_
# @Time : 2023/5/23 9:44
# @Author : 
# @File : page
# @Project : meilan
from rest_framework.pagination import PageNumberPagination


class PageNum(PageNumberPagination):
    page_size = 10  # 默认每页显示多少天数据
    page_size_query_param = 'page_size'  # 前端在查询字符串的关键字，用来控制也没显示多少条数据，默认为None
    max_page_size = 50  # 前端在控制每页最多显示多少条
    page_query_param = 'page'  # 前端在查询字符串的关键字，用来指定是哪一页数据，默认为page


from rest_framework.pagination import LimitOffsetPagination


class LimitNum(LimitOffsetPagination):
    default_limit = 5  # 默认能看几条数据
    limit_query_param = 'limit'  # 前端查询关键字，用来控制显示多少条数据
    max_limit = 50  # 前端控制每页最多显示多少条数据
    offset_query_param = 'offset'  # 前端查询关键字，偏移多少条数据
