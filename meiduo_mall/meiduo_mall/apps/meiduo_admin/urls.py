from django.conf.urls import url
from meiduo_admin.views import users, statistical, channels, skus, orders, perms, spus

urlpatterns = [
    # 进行url配置
    # 管理员登录
    url(r'^authorizations/$', users.AdminAuthView.as_view()),

    # 数据统计
    url(r'^statistical/total_count/$', statistical.TotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.DayIncrementView.as_view()),
    url(r'^statistical/day_active/$', statistical.DayActiveView.as_view()),
    url(r'^statistical/day_orders/$', statistical.DayOrdersView.as_view()),
    url(r'^statistical/month_increment/$', statistical.MonthIncrementView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayViewsView.as_view()),

    # 普通用户管理
    url(r'^users/$', users.UserInfoView.as_view()),

    # 频道管理
    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    url(r'^goods/categories/$', channels.ChannelCategoryView.as_view()),

    # 图片管理
    url(r'^skus/simple/$', skus.SKUSimpleView.as_view()),

    # SKU管理
    url(r'^goods/simple/$', skus.SPUSimpleView.as_view()),
    url(r'^goods/(?P<pk>\d+)/specs/$', skus.SPUSpecView.as_view()),

    # 权限管理
    url(r'^permission/content_types/$', perms.PermissionViewSet.as_view({
        'get': 'content_types'
    })),

    # 用户组管理
    url(r'^permission/simple/$', perms.GroupViewSet.as_view({
        'get': 'simple'
    })),

    # 管理员管理
    url(r'^permission/groups/simple/$', perms.AdminViewSet.as_view({
        'get': 'simple'
    })),

    # SPU管理
    url(r'^goods/brands/simple/$', spus.BrandSimpleView.as_view()),

    # 选项管理
    url(r'^goods/specs/simple/$', spus.SpecSimpleView.as_view()),
]

# 频道管理
from rest_framework.routers import DefaultRouter
# 创建Router对象
router = DefaultRouter()
# 注册视图集
router.register('goods/channels', channels.ChannelViewSet, base_name='channels')
# 添加路由数据
urlpatterns += router.urls

# 图片管理
router = DefaultRouter()
router.register('skus/images', skus.SKUImageViewSet, base_name='images')
urlpatterns += router.urls

# SKU管理
router = DefaultRouter()
router.register('skus', skus.SKUViewSet, base_name='skus')
urlpatterns += router.urls

# 订单管理
router = DefaultRouter()
router.register('orders', orders.OrderInfoViewSet, base_name='orders')
urlpatterns += router.urls

# 权限管理
router = DefaultRouter()
router.register('permission/perms', perms.PermissionViewSet, base_name='perms')
urlpatterns += router.urls

# 用户组管理
router = DefaultRouter()
router.register('permission/groups', perms.GroupViewSet, base_name='groups')
urlpatterns += router.urls

# 管理员管理
router = DefaultRouter()
router.register('permission/admins', perms.AdminViewSet, base_name='admins')
urlpatterns += router.urls

# SPU管理
router = DefaultRouter()
router.register('goods', spus.SPUViewSet, base_name='goods')
urlpatterns += router.urls

router = DefaultRouter()
router.register('goods/channel/categories', spus.CategoryViewSet, base_name='categories')
urlpatterns += router.urls

# 规格管理
router = DefaultRouter()
router.register('goods/specs', spus.SPUSpecViewSet, base_name='specs')
urlpatterns += router.urls

# 选项管理
router = DefaultRouter()
router.register('specs/options', spus.SpecOptionViewSet, base_name='options')
urlpatterns += router.urls

# 品牌管理
router = DefaultRouter()
router.register('goods/brands', spus.BrandViewSet, base_name='brands')
urlpatterns += router.urls
