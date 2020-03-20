# from django.shortcuts import render
import json
import re

from QQLoginTool.QQtool import OAuthQQ
from django import http
from django.conf import settings
from django_redis import get_redis_connection

# Create your views here.
from django.contrib.auth import login
from django.views import View
import logging

from oauth.models import OAuthQQUser
from oauth.utils import generate_access_token, check_access_token
from users.models import User

logger = logging.getLogger('django')


class QQURLView(View):
    def get(self, request):
        next = request.GET.get('next')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
        login_url = oauth.get_qq_url()
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'login_url': login_url})


class QQUserView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少必传参数')

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)

        try:
            token = oauth.get_access_token(code)
            openid = oauth.get_open_id(token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('获取openID失败')

        try:
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except Exception as e:
            access_token = generate_access_token(openid)
            return http.JsonResponse({'code': 300,
                                      'errmsg': 'ok',
                                      'access_token': access_token})
        else:
            user = oauth_qq.user
            login(request, user)
            response = http.JsonResponse({'code': 0,
                                          'errmsg': 'ok'})
            response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
            return response

    def post(self, request):
        dict = json.loads(request.body.decode())
        mobile = dict.get('mobile')
        password = dict.get('password')
        sms_code = dict.get('sms_code')
        access_token = dict.get('access_token')

        # 校验参数
        if not all([mobile, password, sms_code, access_token]):
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式不正确')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码格式不正确')
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if not sms_code_server:
            return http.HttpResponseForbidden('验证码已过期')
        if sms_code_server.decode() != sms_code:
            return http.HttpResponseForbidden('验证码不正确')

        # 解密
        openid = check_access_token(access_token)
        if not openid:
            return http.HttpResponseForbidden('请求access_token错误')

        # 保存数据
        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            user = User.objects.create_user(username=mobile,
                                            password=password,
                                            mobile=mobile)
        else:
            # 用户已存在，判断密码
            if not user.check_password(password):
                return http.HttpResponseForbidden('密码错误')

        # 保存到QQ表
        try:
            OAuthQQUser.objects.create(openid=openid,
                                       user=user)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('用户存储失败')

        # 状态保持
        login(request, user)
        response = http.JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        return response
