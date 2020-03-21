from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from meiduo_admin.serializers.perms import PermissionSerializer, ContentTypeSerializer, GroupSerializer, \
    PermSimpleSerializer, AdminUserSerializer, GroupSimpleSerializer

from users.models import User


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    # GET /meiduo_admin/permission/perms/ -> list
    # POST /meiduo_admin/permission/perms/ -> create
    # GET /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/permission/perms/(?P<pk>\d+)/ -> destroy
    # GET /meiduo_admin/permission/content_types/ -> content_types

    def content_types(self, request):
        """
        获取所有的权限类型的数据：
        """
        c_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(c_types, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的update
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=204)


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    #  GET /meiduo_admin/permission/groups/ -> list
    #  POST /meiduo_admin/permission/groups/ -> create
    #  GET /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> retrieve
    #  PUT /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> update
    #  DELETE /meiduo_admin/permission/groups/(?P<pk>\d+)/ -> destroy
    #  GET /meiduo_admin/permission/simple/ -> simple

    def simple(self, request):
        """
        获取所有权限的简单数据：
        """
        perms = Permission.objects.all()
        serializer = PermSimpleSerializer(perms, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的update
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=204)


class AdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminUserSerializer

    # GET /meiduo_admin/permission/admins/ -> list
    # POST /meiduo_admin/permission/admins/ -> create
    # GET /meiduo_admin/permission/admins/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/permission/admins/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/permission/admins/(?P<pk>\d+)/ -> destroy
    # GET /meiduo_admin/permission/groups/simple/ -> simple

    def simple(self, request):
        """
        获取用户组的简单数据：
        """
        groups = Group.objects.all()
        serializer = GroupSimpleSerializer(groups, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的create
    #     return Response(serializer.data, status=201)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save() # 调用序列化器类中的update
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=204)
