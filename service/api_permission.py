import json
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from service.api_service import WclApiService


class ApiPermissionCheck(MiddlewareMixin):
    """
    api调用权限校验中间件
    """
    def process_request(self, request):
        # if request.path.startswith('/api/v1.0/accounts/login'):
        #     # 登录接口特殊处理
        #     return
        if request.path.startswith('/api/'):
            flag, msg = self.token_permission_check(request)
            if not flag:
                return HttpResponse(json.dumps(dict(code=-1, msg='token校验失败：{}'.format(msg), data={})), content_type="application/json")

    def token_permission_check(self, request):
        signature = request.META.get('HTTP_SIGNATURE')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        token_name = request.META.get('HTTP_TOKENNAME')
        print(signature, timestamp, token_name)

        # if not app_name:
        #     return False, '未提供appname(调用loonflow接口需要鉴权，请根据文档中"调用授权"部分说明来调用)'
        token_obj, msg = WclApiService.get_token_by_token_name(token_name=token_name)
        if not token_obj:
            return False, 'token name不存在，请联系管理员申请token'
        return WclApiService.signature_check(timestamp, signature, token_obj.token)
