from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from goods.models import SKUImage, SKU, SPU, SPUSpecification
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer, SPUSimpleSerializer, \
    SPUSpecSerializer

from django.db.models import Q

class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer

    # GET /meiduo_admin/skus/images/ -> list
    # POST /meiduo_admin/skus/images/ -> create
    # GET /meiduo_admin/skus/images/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/skus/images/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/skus/images/(?P<pk>\d+)/ -> destroy

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


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = SKUSimpleSerializer
    queryset = SKU.objects.all()

    # 关闭分页
    pagination_class = None


class SKUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    # queryset = None
    serializer_class = SKUSerializer

    def get_queryset(self):
        # 获取keyword
        keyword = self.request.query_params.get('keyword')

        if keyword:
            # 查询名称或副标题中含有keyword的SKU数据
            skus = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword)) # Q对象
        else:
            # 查询所有SKU数据
            skus = SKU.objects.all()

        return skus

    # GET /meiduo_admin/skus/ -> list
    # POST /meiduo_admin/skus/ -> create
    # GET /meiduo_admin/skus/(?P<pk>\d+)/ -> retrieve
    # PUT /meiduo_admin/skus/(?P<pk>\d+)/ -> update
    # DELETE /meiduo_admin/skus/(?P<pk>\d+)/ -> destroy

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

# GET /meiduo_admin/goods/simple/
class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = SPUSimpleSerializer
    queryset = SPU.objects.all()

    # 关闭分页
    pagination_class = None


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = SPUSpecSerializer
    # queryset = SPUSpecification.objects.filter(spu_id=pk)

    def get_queryset(self):
        """
        self.kwargs: 字典，保存了从url地址中提取所有命名参数
        """
        pk = self.kwargs['pk']
        return SPUSpecification.objects.filter(spu_id=pk)

    # 关闭分页
    pagination_class = None

    # def get(self, request):
    #     return self.list(request)

    # def get(self, request, pk):
    #     """
    #     获取spu规格的数据:
    #     1. 查询数据库获取spu关联所有的规格数据
    #     2. 将规格数据序列化并返回
    #     """
    #     # 1. 查询数据库获取spu关联所有的规格数据
    #     # spu = SPU.objects.get(id=pk)
    #     # specs = spu.specs.all()
    #
    #     spu_specs = self.get_queryset()
    #
    #     # 2. 将规格数据序列化并返回
    #     serializer = self.get_serializer(spu_specs, many=True)
    #     return Response(serializer.data)





















