import requests
from service.constant import CONSTANT_SERVICE
from django.conf import settings
import json
import traceback


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
            # print(url)
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
