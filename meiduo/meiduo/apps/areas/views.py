# from django.shortcuts import render

# Create your views here.
from django import http
from django.core.cache import cache
from django.views import View
from .models import Area
import logging

logger = logging.getLogger('django')


class ShowProvincialView(View):
    def get(self, request):
        data_list = cache.get('province')
        if not data_list:
            try:
                province_model_list = Area.objects.filter(parent__isnull=True)
                data_list = list()
                for province in province_model_list:
                    data_list.append({'id': province.id, 'name': province.name})
                cache.set('province', data_list, 3600)
            except Exception as e:
                logger.error(e)
                return http.HttpResponseForbidden('获取信息失败')
        return http.JsonResponse({"code": "0",
                                  "errmsg": "OK",
                                  'province_list': data_list})


class ExhibitionCityCountyView(View):
    def get(self, request, pk):
        sub_data = cache.get('sub_%s' % pk)
        if not sub_data:
            try:
                citycounty_list = Area.objects.filter(parent=pk)
                province = Area.objects.get(pk=pk)
                subs = list()
                for citycounty in citycounty_list:
                    subs.append({'id': citycounty.id, 'name': citycounty.name})
                sub_data = {'id': province.id,
                            'name': province.name,
                            'subs': subs}

                cache.set('sub_%s' % pk, sub_data, 3600)
            except Exception as e:
                logger.error(e)
                return http.HttpResponseForbidden('获取数据失败')

        return http.JsonResponse({"code": "0",
                                  "errmsg": "OK",
                                  'sub_data': sub_data})
