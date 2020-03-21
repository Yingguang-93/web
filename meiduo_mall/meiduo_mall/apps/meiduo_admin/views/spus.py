from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet

from goods.models import SPU, Brand, GoodsCategory, SPUSpecification, SpecificationOption
from meiduo_admin.serializers.spus import SPUSerializer, BrandSimpleSerializer, CategorySerializer, SPUSpecSerializer, \
    SpecOptionSerializer, SpecSimpleSerializer, BrandSerializer


class SPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    lookup_value_regex = '\d+'

    queryset = SPU.objects.all()
    serializer_class = SPUSerializer


# GET /meiduo_admin/goods/brands/simple/
class BrandSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]

    queryset = Brand.objects.all()
    serializer_class = BrandSimpleSerializer

    # 关闭分页
    pagination_class = None


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]

    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            return GoodsCategory.objects.filter(parent=None)
        else:
            pk = self.kwargs['pk']
            return GoodsCategory.objects.filter(parent_id=pk)

    def retrieve(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 关闭分页
    pagination_class = None


class SPUSpecViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = SPUSpecification.objects.all()
    serializer_class = SPUSpecSerializer


class SpecOptionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = SpecificationOption.objects.all()
    serializer_class = SpecOptionSerializer


class SpecSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]

    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSimpleSerializer

    # 关闭分页
    pagination_class = None


class BrandViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
