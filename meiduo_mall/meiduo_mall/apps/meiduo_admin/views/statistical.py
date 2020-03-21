from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import mixins
from django.utils import timezone

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import GoodsVisitSerializer
from users.models import User


# GET /meiduo_admin/statistical/total_count/
class TotalCountView(APIView):
    # 仅管理员才能进行访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        获取网站用户的总数：
        1. 查询数据统计网站用户的总数
        2. 返回响应
        """
        # 1. 查询数据统计网站用户的总数
        count = User.objects.count()

        # 2. 返回响应
        now_date = timezone.now() # 年-月-日 时:分:秒

        response_data = {
            'count': count,
            'date': now_date.date()
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/day_increment/
class DayIncrementView(APIView):
    # 仅管理员才能进行访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        统计网站日增用户数量：
        1. 查询数据库统计网站日增用户数量
        2. 返回响应
        """
        # 1. 查询数据库统计网站日增用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_date).count()

        # 2. 返回响应
        response_data = {
            'count': count,
            'date': now_date.date()
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/day_active/
class DayActiveView(APIView):
    # 仅管理员才能进行访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        统计网站日活跃用户数量：
        1. 查询数据库统计网站日活跃用户数量
        2. 返回响应
        """
        # 1. 查询数据库统计网站日活跃用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_date).count()

        # 2. 返回响应
        response_data = {
            'count': count,
            'date': now_date.date()
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/day_orders/
class DayOrdersView(APIView):
    # 仅管理员才能进行访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        统计网站日下单用户数量：
        1. 查询数据库统计网站日下单用户数量
        2. 返回响应
        """
        # 1. 查询数据库统计网站日下单用户数量
        now_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_date).distinct().count()

        # 2. 返回响应
        response_data = {
            'count': count,
            'date': now_date.date()
        }

        return Response(response_data)


# GET /meiduo_admin/statistical/month_increment/
class MonthIncrementView(APIView):
    # 仅管理员才能进行访问
    permission_classes = [IsAdminUser]

    def get(self, request):
        """
        统计网站最近30天每天新增用户数量:
        1. 查询数据库统计网站最近30天每天新增用户数量
        2. 返回响应
        """
        # 1. 查询数据库统计网站最近30天每天新增用户数量
        # 时间范围：当天时间-29天 <-> 当天时间
        # 结束时间
        end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # 起始时间
        begin_date = end_date - timezone.timedelta(days=29)

        # 数据统计
        cur_date = begin_date

        month_li = []
        while cur_date <= end_date:
            # 统计cur_date这一天新增用户数据
            next_date = cur_date + timezone.timedelta(days=1)
            count = User.objects.filter(date_joined__gte=cur_date, date_joined__lt=next_date).count()

            # 添加数据
            month_li.append({
                'count': count,
                'date': cur_date.date()
            })

            # 当前日期向后加1天
            cur_date = next_date

        # 2. 返回响应
        return Response(month_li)


# GET /meiduo_admin/statistical/goods_day_views/
class GoodsDayViewsView(ListAPIView):
    permission_classes = [IsAdminUser]
    # 指定视图使用的序列化器类
    serializer_class = GoodsVisitSerializer

    # queryset = GoodsVisitCount.objects.filter(date=now_date)

    def get_queryset(self):
        now_date = timezone.now().date()
        return GoodsVisitCount.objects.filter(date=now_date) # QuerySet

    # 关闭分页
    pagination_class = None

    # def get(self, request):
    #     return self.list(request)

    # def get(self, request):
    #     """
    #     获取日分类商品的访问量:
    #     1. 查询数据库获取当天日分类商品访问的数据
    #     2. 将数据序列化并返回
    #     """
    #     # 1. 查询数据库获取当天日分类商品访问的数据
    #     g_visits = self.get_queryset()
    #
    #     # 2. 将数据序列化并返回
    #     serializer = self.get_serializer(g_visits, many=True)
    #     return Response(serializer.data)

































