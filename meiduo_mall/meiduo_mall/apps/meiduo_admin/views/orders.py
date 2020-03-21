from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.db.models import Q

# 订单数据的获取 -> list
# 订单详情的获取 -> retrieve
from meiduo_admin.serializers.orders import OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer
from orders.models import OrderInfo


class OrderInfoViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]

    # queryset = None
    # serializer_class = OrderListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            # status
            return OrderStatusSerializer

    def get_queryset(self):
        # 获取keyword
        keyword = self.request.query_params.get('keyword')

        if keyword:
            # 查询订单编号等于keyword或者和订单关联订单商品记录对应sku商品的名称中含有keyword
            # orders = OrderInfo.objects.filter(Q(order_id=keyword) |
            #                                   Q(skus__sku__name__contains=keyword)).distinct()
            orders = OrderInfo.objects.filter(skus__sku__name__contains=keyword)
        else:
            # 查询所有订单数据
            orders = OrderInfo.objects.all()

        return orders

    # GET /meiduo_admin/orders/ -> list
    # GET /meiduo_admin/orders/(?P<pk>\d+)/ —> retrieve
    # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/ -> status

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        return self.update(request, pk)

    # @action(methods=['put'], detail=True)
    # def status(self, request, pk):
    #     """
    #     指定订单状态的修改：
    #     1. 根据pk获取指定的订单
    #     2. 获取status并进行校验
    #     3. 修改指定订单状态
    #     4. 返回响应
    #     """
    #     # 1. 根据pk获取指定的订单
    #     order = self.get_object()
    #
    #     # 2. 获取status并进行校验
    #     serializer = self.get_serializer(order, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 3. 修改指定订单状态
    #     serializer.save() # 调用序列化器类中的update
    #
    #     # 4. 返回响应
    #     return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
