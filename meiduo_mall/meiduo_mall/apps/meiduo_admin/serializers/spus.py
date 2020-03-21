from rest_framework import serializers

from goods.models import SPU, Brand, GoodsCategory, SPUSpecification, SpecificationOption


class SPUSerializer(serializers.ModelSerializer):
    """SPU商品序列化器类"""
    brand = serializers.StringRelatedField(label='品牌')
    brand_id = serializers.IntegerField(label='品牌ID')
    category1_id = serializers.IntegerField(label='一级分类ID')
    category2_id = serializers.IntegerField(label='二级分类ID')
    category3_id = serializers.IntegerField(label='三级分类ID')

    class Meta:
        model = SPU
        exclude = ('category1', 'category2', 'category3', 'create_time', 'update_time')

    def validate_brand_id(self, value):
        # 品牌是否存在
        try:
            Brand.objects.get(id=value)
        except Brand.DoesNotExist:
            raise serializers.ValidationError('品牌不存在')

        return value

    def validate(self, attrs):
        category1_id = attrs.get('category1_id')
        category2_id = attrs.get('category2_id')
        category3_id = attrs.get('category3_id')

        # 一级分类是否存在
        try:
            GoodsCategory.objects.get(id=category1_id, parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')

        # 二级分类是否有误
        try:
            GoodsCategory.objects.get(id=category2_id, parent_id=category1_id)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('二级分类有误')

        # 三级分类是否有误
        try:
            GoodsCategory.objects.get(id=category3_id, parent_id=category2_id)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('三级分类有误')

        return attrs


class BrandSimpleSerializer(serializers.ModelSerializer):
    """商品品牌序列化器类"""
    class Meta:
        model = Brand
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    """商品分类序列化器类"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class SPUSpecSerializer(serializers.ModelSerializer):
    """商品规格序列化器类"""
    spu = serializers.StringRelatedField(label='SPU商品')
    spu_id = serializers.IntegerField(label='SPU商品ID')

    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time')

    def validate_spu_id(self, value):
        # SPU是否存在
        try:
            SPU.objects.get(id=value)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU不存在')

        return value


class SpecOptionSerializer(serializers.ModelSerializer):
    """选项序列化器类"""
    spec = serializers.StringRelatedField(label='规格')
    spec_id = serializers.IntegerField(label='规格id')

    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')

    def validate_spec_id(self, value):
        # 规格是否存在
        try:
            SPUSpecification.objects.get(id=value)
        except SPUSpecification.DoesNotExist:
            raise serializers.ValidationError('规格不存在')

        return value


class SpecSimpleSerializer(serializers.ModelSerializer):
    """规格序列化器类"""
    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')


class BrandSerializer(serializers.ModelSerializer):
    """品牌序列化器类"""
    class Meta:
        model = Brand
        exclude = ('create_time', 'update_time')