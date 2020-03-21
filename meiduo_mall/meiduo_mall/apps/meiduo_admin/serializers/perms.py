from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.models import User


class PermissionSerializer(serializers.ModelSerializer):
    """权限的序列化器类"""
    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    """权限类型的序列化器类"""
    class Meta:
        model = ContentType
        fields = ('id', 'name')


class GroupSerializer(serializers.ModelSerializer):
    """用户组序列化器类"""
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class PermSimpleSerializer(serializers.ModelSerializer):
    """权限序列化器类"""
    class Meta:
        model = Permission
        fields = ('id', 'name')


class AdminUserSerializer(serializers.ModelSerializer):
    """管理员用户序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile', 'groups', 'user_permissions', 'password')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True # 是否能够传递''字符串
            }
        }

    def create(self, validated_data):
        validated_data['is_staff'] = True

        # 添加管理员用户
        user = super().create(validated_data)
        # user = User.objects.create(**validated_data)

        # 设置密码
        password = validated_data.get('password')

        if not password:
            # 设置默认密码
            password = '123456abc'

        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        # 修改管理员用户的数据
        super().update(instance, validated_data)

        # 是否需要修改密码
        if password:
            instance.set_password(password)
            instance.save()

        return instance


class GroupSimpleSerializer(serializers.ModelSerializer):
    """用户组的序列化器类"""
    class Meta:
        model = Group
        fields = ('id', 'name')


















