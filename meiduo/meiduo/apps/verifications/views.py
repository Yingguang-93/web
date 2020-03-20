# from django.shortcuts import render
import random
import logging

from celery_tasks.sms.tasks import ccp_send_sms_code
from meiduo.libs.yuntongxun.ccp_sms import CCP

logger = logging.getLogger('django')
from django import http
from django_redis import get_redis_connection
# Create your views here.
from django.views import View
from meiduo.libs.captcha.captcha import captcha


class ImageCodeView(View):
    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('sms_%s' % uuid, 300, text)
        return http.HttpResponse(image, content_type='image/jpg')


class SMSCodeView(View):
    def get(self, request, mobile):
        redis_conn = get_redis_connection('verify_code')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '发送短信过于频繁'})
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([mobile, image_code_client, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')

        image_code_server = redis_conn.get('sms_%s' % uuid)
        if image_code_server is None:
            return http.HttpResponseForbidden('验证码已过期')
        try:
            redis_conn.delete('img_%s' % uuid)
        except Exception as e:
            logger.error(e)

        if image_code_server.decode().lower() != image_code_client.lower():
            return http.HttpResponseForbidden('验证码不正确')

        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        redis_conn.setex('sms_%s' % mobile,
                         300,
                         sms_code)
        redis_conn.setex('send_flag_%s' % mobile, 60, 1)

        # 9. 发送短信验证码
        # 短信模板
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # ccp_send_sms_code.delay(mobile, sms_code)

        # 10. 响应结果
        return http.JsonResponse({'code': 0,
                                  'errmsg': '发送短信成功'})
