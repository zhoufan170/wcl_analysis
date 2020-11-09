from django.views import View
from service.base_service import BaseService
from service.api_service import api_response
from service.constant import CONSTANT_SERVICE
from taq.models import ViscidusPoisonTick
from service.taq_service import TaqService

# Create your views here.


class ViscidusPoisonTick(View):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        id = request_data.get('id', '')

        if not id:
            code, msg, data = 30000, '日志id缺失', {}
            return api_response(code, msg, data)

        success, result, msg = TaqService.get_viscidus_poison_tick_detail_api(log_id=id)

        if not success:
            code, msg, data = 30000, msg, {}
            return api_response(code, msg, data)

        code, msg, data = 20000, msg, result
        return api_response(code, msg, result)


class BossNatureProtection(View):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        id = request_data.get('id', '')

        if not id:
            code, msg, data = 30000, '日志id缺失', {}
            return api_response(code, msg, data)

        success, result, msg = TaqService.get_boss_nature_protection_detail_api(log_id=id)

        if not success:
            code, msg, data = 30000, msg, {}
            return api_response(code, msg, data)

        code, msg, data = 20000, msg, result
        return api_response(code, msg, result)
