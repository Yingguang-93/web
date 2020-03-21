from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(serializers.ModelSerializer):
    """频道的序列化器类"""
    group_id = serializers.IntegerField(label='频道组id')
    category_id = serializers.IntegerField(label='一级分类id')

    group = serializers.StringRelatedField(label='频道组')
    category = serializers.StringRelatedField(label='一级分类')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')

    def validate_group_id(self, value):
        # 频道组是否存在
        try:
            GoodsChannelGroup.objects.get(id=value)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')

        return value

    def validate_category_id(self, value):
        # 一级分类是否存在
        try:
            GoodsCategory.objects.get(id=value)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')

        return value

    # GoodsChannel.objects.create(**validated_data)

class ChannelTypeSerializer(serializers.ModelSerializer):
    """频道组的序列化器类"""
    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class ChannelCategorySerializer(serializers.ModelSerializer):
    """分类的序列化器类"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')





















