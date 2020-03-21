from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultPagination(PageNumberPagination):
    # 指定分页的默认页容量
    page_size = 3
    # 指定获取分页数据时，指定页容量参数的名称
    page_size_query_param = 'pagesize'
    # 指定分页时的最大页容量
    max_page_size = 20

    def get_paginated_response(self, data):
        """重写分页类响应数据格式函数"""
        return Response(OrderedDict([
            ('counts', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))
