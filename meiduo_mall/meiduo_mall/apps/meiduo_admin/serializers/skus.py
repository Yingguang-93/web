from django.db import transaction
from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, SPU, SPUSpecification, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    """图片的序列化器类"""
    sku_id = serializers.IntegerField(label='SKU商品ID')

    sku = serializers.StringRelatedField(label='SKU商品')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        # 校验SKU商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('SKU商品不存在')

        return value

    # SKUImage.objects.create(**validated_data)
    def create(self, validated_data):
        # 上传图片并保存记录
        sku_image = super().create(validated_data)

        # 设置默认图片
        sku = sku_image.sku

        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()

        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU商品的序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    """sku具体规格选项的序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """sku商品的序列化器类"""
    spu_id = serializers.IntegerField(label='SPU ID')

    # 使用指定的序列化器进行关联对象的嵌套序列化
    specs = SKUSpecSerializer(label='SKU具体规格', many=True)

    category = serializers.StringRelatedField(label='第三级分类')

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'spu', 'comments', 'default_image')

        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        # 1. SPU是否存在
        spu_id = attrs['spu_id']

        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU不存在')

        # 获取第三级分类id
        attrs['category_id'] = spu.category3.id

        # 2. SPU规格数据是否合法
        # 查询数据库获取和spu关联的规格数据
        specs = spu.specs.all() # QuerySet
        # 获取客户端传递规格数据
        spu_specs = attrs['specs'] # list

        # 2.1 SPU规格的数量是否一致
        specs_count = specs.count()
        spu_specs_count = len(spu_specs)

        if specs_count != spu_specs_count:
            raise serializers.ValidationError('规格数量不一致')

        # 2.2 SPU规格的数据是否一致 [11, 12, 13] [11, 12, 14]
        spec_ids = [spec.id for spec in specs] # [11, 12, 13]
        spu_spec_ids = [spec.get('spec_id') for spec in spu_specs] # [11, 13, 12]

        # 排序
        spec_ids.sort()
        spu_spec_ids.sort()

        if spec_ids != spu_spec_ids:
            raise serializers.ValidationError('规格数据有误')

        # 3. 规格选项数据是否合法
        for spec in spu_specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

            # 获取规格下所有的选项
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            option_ids = [option.id for option in options]

            if option_id not in option_ids:
                raise serializers.ValidationError('选项数据有误')

        return attrs

    def create(self, validated_data):
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 添加SKU的数据
            sku = super().create(validated_data)

            # 添加SKU具体规格选项的数据
            for spec in specs:
                spec_id = spec.get('spec_id')
                option_id = spec.get('option_id')

                SKUSpecification.objects.create(
                    sku=sku,
                    spec_id=spec_id,
                    option_id=option_id
                )

        return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')

        with transaction.atomic():
            # 修改SKU数据
            super().update(instance, validated_data)

            # 修改SKU具体规格的数据
            instance.specs.all().delete()

            for spec in specs:
                spec_id = spec.get('spec_id')
                option_id = spec.get('option_id')

                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec_id,
                    option_id=option_id
                )
        return instance





class SPUSimpleSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""
    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptionSerializer(serializers.ModelSerializer):
    """选项序列化器类"""
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecSerializer(serializers.ModelSerializer):
    """规格序列化器类"""
    options = SpecOptionSerializer(label='选项', many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'options')






















