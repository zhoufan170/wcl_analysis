import requests
from service.constant import CONSTANT_SERVICE
from django.conf import settings
import json
import traceback
import time
import hashlib
from api.models import ApiToken
from django.http import HttpResponse


class WclApiService():
    def __init__(self):
        pass

    @classmethod
    def get_api(cls, api, view, code, params):
        if api not in CONSTANT_SERVICE.register_api():
            return False, 'api %s has not registered' % api

        if api == CONSTANT_SERVICE.FIGHT_API:
            url = '%s%s%s?api_key=%s' % (settings.WCL_SCHEMA, api, code, settings.WCL_API_KEY)
        elif api in CONSTANT_SERVICE.TABLES_API or CONSTANT_SERVICE.EVENT_API:
            url = '%s%s%s/%s?api_key=%s' % (settings.WCL_SCHEMA, api, view, code, settings.WCL_API_KEY)
            if params and params is not {}:
                for key in params.keys():
                    url = '%s&%s=%s' % (url, str(key), str(params.get(key)))

        try:
            print(url)
            response = requests.get(url=url)
            if response.status_code != 200:
                if response.status_code == 400:
                    error_dict = json.loads(response.text)
                    return False, error_dict.get("error")
                else:
                    return False, 'call wcl api fail, http_code = %d' % response.status_code

            result = json.loads(response.text)
        except Exception as e:
            return False, traceback.format_exc()

        return True, result

    @classmethod
    def signature_check(cls, timestamp, signature, md5_key):
        """
        签名校验
        :param timestamp:
        :param signature:
        :param md5_key:
        :return:
        """
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        if tar_str == signature:
            # 时间验证，120s
            time_now_int = int(time.time())
            # if abs(time_now_int - int(timestamp)) <= 120:
            if abs(time_now_int - int(timestamp)) <= 12000000000000000:
                return True, ''
            else:
                msg = '时间戳过期,请保证在120s内'
        else:
            msg = '签名校验失败'
        return False, msg

    @classmethod
    def gen_signature(cls, token):
        """
        生成签名信息
        :param app_name:
        :return:
        """
        from api.models import ApiToken
        api_obj = ApiToken.objects.filter(token=token, is_deleted=0).first()
        md5_key = api_obj.token
        timestamp = str(int(time.time()))
        ori_str = timestamp + md5_key
        tar_str = hashlib.md5(ori_str.encode(encoding='utf-8')).hexdigest()
        return True, dict(signature=tar_str, timestamp=timestamp)

    @classmethod
    def get_token_by_token_name(cls, token_name):
        """
        获取token对象
        :param token_name:
        :return:
        """
        app_token_obj = ApiToken.objects.filter(name=token_name, is_deleted=0).first()
        return app_token_obj, ''


def api_response(code, msg='', data=''):
    """
    格式化返回
    :param code:
    :param msg:
    :param data:
    :return:
    """
    return HttpResponse(json.dumps(dict(code=code, data=data, message=msg)), content_type="application/json")


