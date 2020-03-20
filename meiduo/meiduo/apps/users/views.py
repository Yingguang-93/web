import json
import re
# 从 celery_tasks 中导入:
from celery_tasks.email.tasks import send_verify_email

from django import http
# from django.shortcuts import render
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django_redis import get_redis_connection

from meiduo.utils.views import LoginStatusCheckMixin
from .models import User, Address
import logging

logger = logging.getLogger('django')


class UserNameCountView(View):

    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'count': count})


class MobileCountView(View):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'count': count})


class RegisterView(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        password2 = dict.get('password2')
        mobile = dict.get('mobile')
        sms_code = dict.get('sms_code')
        allow = dict.get('allow')

        if not all([username, password, password2, mobile, sms_code]):
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('用户名为5-20位的字符串')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码为8-20位的字符串')

        if password != password2:
            return http.HttpResponseForbidden('密码不一致')

        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式不正确')

        if allow != 'true':
            return http.HttpResponseForbidden('请勾选用户同意')

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None:
            return http.HttpResponseForbidden('验证码已过期')

        if sms_code_server.decode() != sms_code:
            return http.HttpResponseForbidden('验证码不一致')

        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('存储失败')

        login(request, user)
        response = http.JsonResponse({'code': 0,
                                      'errmsg': 'ok'})
        response.set_cookie('username', username, 3600 * 24 * 14)
        # 响应登录结果
        return response


class LoginView(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')

        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('用户名格式错误')

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码格式错误')

        user = authenticate(username=username, password=password)
        if user is None:
            return http.HttpResponse(status=400)
            # 实现状态保持
        login(request, user)

        # 设置状态保持的周期
        if remembered != True:
            # 不记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            # 记住用户：None 表示两周后过期
            request.session.set_expiry(None)

        response = http.JsonResponse({'code': 0,
                                      'errmsg': 'ok'})
        response.set_cookie('username', username, 3600 * 24 * 14)
        # 响应登录结果
        return response


class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = http.JsonResponse({'code': 0,
                                      'errmsg': 'ok'})
        response.delete_cookie('username')
        return response


class UserInfoView(LoginStatusCheckMixin, View):
    def get(self, request):
        user = request.user
        info_data = {'username': user.username,
                     'mobile': user.mobile,
                     'email': user.email,
                     'email_active': user.email_active}
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'info_data': info_data})


class UserEmailView(View):
    def put(self, request):
        dict = json.loads(request.body.decode())
        email = dict.get('email')
        if not email:
            return http.HttpResponseForbidden('邮箱未填写')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('邮箱格式不正确')

        # 保存邮箱
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('保存邮箱失败')

        # 调用发送的函数:
        verify_url = request.user.generate_verify_email_url()
        send_verify_email.delay(email, verify_url)

        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class VerifyEmailView(View):
    """验证邮箱"""

    def put(self, request):
        """实现邮箱验证逻辑"""
        # 接收参数
        token = request.GET.get('token')

        # 校验参数：判断 token 是否为空和过期，提取 user
        if not token:
            return http.HttpResponseBadRequest('缺少token')

        # 调用上面封装好的方法, 将 token 传入
        user = User.check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')

        # 修改 email_active 的值为 True
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活邮件失败')

        # 返回邮箱验证结果
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class IncreaseAddressVIew(View):
    def post(self, request):
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式错误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('固定电话格式错误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('邮箱格式错误')

        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('存储失败')

        address_dict = {
            "title": address.title,
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email,
        }

        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'addresses': address_dict})


class ShowAddressView(View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user, is_deleted=False)
        address_list = list()
        for address in addresses:
            dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            default_address = request.user.default_address
            if default_address.id == address.id:
                address_list.insert(0, dict)
            else:
                address_list.append(dict)
        id = request.user.default_address_id
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'default_address_id': id,
                                  'addresses': address_list})


class ChangeDestryAddressView(View):
    def put(self, request, address_id):
        dict = json.loads(request.body.decode())
        receiver = dict.get('receiver')
        province_id = dict.get('province_id')
        city_id = dict.get('city_id')
        district_id = dict.get('district_id')
        place = dict.get('place')
        mobile = dict.get('mobile')
        tel = dict.get('tel')
        email = dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号格式错误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('固定电话格式错误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('邮箱格式错误')

        try:
            Address.objects.filter(id=address_id, is_deleted=False).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )

        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('修改失败')
        address = Address.objects.get(id=address_id)
        address_dict = {
            "title": address.title,
            'id': address.id,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email,
        }

        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok',
                                  'addresses': address_dict})

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('修改失败')
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class DefaultView(View):
    def put(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('修改失败')
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class TetilView(View):
    def put(self, request, address_id):
        dict = json.loads(request.body.decode())
        title = dict.get('title')
        try:
            address = Address.objects.get(id=address_id)
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('修改失败')
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})


class ChangePasswordView(View):
    def put(self, request):
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        if not all([old_password, new_password, new_password2]):
            return http.HttpResponseForbidden('缺少必传参数')

        res = request.user.check_password(old_password)
        if not res:
            return http.HttpResponseForbidden('原密码错误')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return http.HttpResponseForbidden('新密码格式错误')
        if new_password != new_password2:
            return http.HttpResponseForbidden('两次密码输入不一致')

        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('修改失败')

        return http.JsonResponse({'code': 0,
                                  'errmsg': 'ok'})
