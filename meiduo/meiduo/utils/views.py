# 通用装饰器
from django import http


def set_func(fun):
    def call_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fun(request)
        else:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '请登录后重试'})
    return call_func


class LoginStatusCheckMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view()
        return set_func(view)
