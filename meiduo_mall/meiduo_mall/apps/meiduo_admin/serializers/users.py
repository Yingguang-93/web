import re
from django.utils import timezone
from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    """管理员登录序列化器类"""
    token = serializers.CharField(label='JWT Token', read_only=True)
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 用户名和密码是否正确
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            # 用户不存在
            raise serializers.ValidationError('用户名或密码错误')
        else:
            # 校验密码
            if not user.check_password(password):
                # 密码错误
                raise serializers.ValidationError('用户名或密码错误')

        # 添加user
        attrs['user'] = user

        # attrs中有什么，validated_data就会有什么
        return attrs

    def create(self, validated_data):
        # 获取user
        user = validated_data['user']

        # 更新用户最新登录时间
        user.last_login = timezone.now()
        user.save()

        # 创建jwt token
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 临时给user对象增加一个token属性
        user.token = token

        return user


class UserInfoSerializer(serializers.ModelSerializer):
    """用户序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_mobile(self, value):
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        # 手机号是否存在
        count = User.objects.filter(mobile=value).count()

        if count > 0:
            raise serializers.ValidationError('手机号已存在')

        return value

    def create(self, validated_data):
        # 创建普通用户并保存到数据库，密码加密保存
        user = User.objects.create_user(**validated_data)

        return user


















