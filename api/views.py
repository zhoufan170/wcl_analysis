# from django.shortcuts import render
from django.views import View
import json
from service.base_service import BaseService
from service.api_service import api_response


class LogListView(View):
    def get(self, request, *args, **kwargs):
        """
        获取日志列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        raid = request_data.get('raid', '')
        wcl_code = request_data.get('code', '')
        page = request_data.get('page', 1)
        per_page = request_data.get('per_page', 5)

        wcl_log_restful_list, msg = BaseService.get_log_list(raid=raid, code=wcl_code, page=page, per_page=per_page)
        if wcl_log_restful_list is not False:
            data = dict(data=wcl_log_restful_list, per_page=msg['per_page'], page=msg['page'], total=msg['total'])
            code, msg = 20000, ''
        else:
            code, data = 30000, {}
        return api_response(code, msg, data)

    def post(self, request, *args, **kwargs):
        """
        新增日志
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        report_code = request_data_dict.get('code', '')
        raid = request_data_dict.get('raid', '')
        if not report_code:
            code, msg, data = 30000, 'code is required', ''
            return api_response(code, msg, data)
        if not raid:
            code, msg, data = 30000, 'raid is required', ''
            return api_response(code, msg, data)
        result, msg = BaseService.load_fight_data(code=report_code, raid=raid)
        if result:
            code, msg, data = 20000, '', {}
        else:
            code, msg, data = 30000, msg, {}
        return api_response(code, msg, data)


class LogDetailView(View):
    def get(self, request, *args, **kwargs):
        request_data = request.GET
        id = request_data.get('id', '')
        if not id:
            code, msg, data = 30000, '日志id缺失', {}
            return api_response(code, msg, data)

        log_obj, msg = BaseService.get_wcl_log_by_id(log_id=id)
        if not log_obj:
            code, msg, data = 30000, '日志不存在', {}
            return api_response(code, msg, data)

        log_details, msg = BaseService.get_log_detail_list_by_id_for_api(log_obj.id)
        if not log_details:
            code, msg, data = 30000, msg, {}
        else:
            code, msg, data = 20000, '', log_details

        return api_response(code, msg, data)


class LogAnalysisRun(View):
    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('utf-8')
        request_data_dict = json.loads(json_str)
        log_id = request_data_dict.get("id", '')
        if not log_id:
            code, msg, data = 30000, '日志id缺失', {}
            return api_response(code, msg, data)

        result, msg = BaseService.run_all_scan_task(log_id=log_id)
        if not result:
            code, msg, data = 30000, msg, {}
        else:
            code, msg, data = 20000, '', {}
        return api_response(code, msg, data)


