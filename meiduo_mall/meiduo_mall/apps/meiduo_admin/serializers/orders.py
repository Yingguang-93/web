from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderListSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')


class SKUSerializer(serializers.ModelSerializer):
    """SKU商品序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image')


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品记录序列化器类"""
    sku = SKUSerializer(label='SKU商品')

    class Meta:
        model = OrderGoods
        fields = ('id', 'price', 'count', 'sku')


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    skus = OrderGoodsSerializer(label='订单商品记录', many=True)
    user = serializers.StringRelatedField(label='下单用户')

    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        exclude = ('address', 'update_time')


class OrderStatusSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')

        extra_kwargs = {
            'order_id': {
                'read_only': True
            }
        }

    def validate_status(self, value):
        # 订单状态是否合法
        if value not in [1, 2, 3, 4, 5, 6]:
            raise serializers.ValidationError('订单状态有误')

        return value













