from django.shortcuts import render, redirect
from base.form import LoadReportForm
from service.base_service import BaseService
from base.models import WCLLog
from service.constant import CONSTANT_SERVICE
import json
from service.taq_service import TaqService

# Create your views here.


def load_report(request):
    if request.META.get("REQUEST_METHOD") == 'GET':
        form = LoadReportForm
        return render(request, 'base/load_report.html', {'form': form, 'heading': 'Upload Your WCL log'})

    elif request.META.get("REQUEST_METHOD") == 'POST':
        post_data = request.POST
        code = post_data.get("code")
        result, msg = BaseService.load_fight_data(code=code)
        if result:
            return redirect('/service/')
        else:
            return render(request, 'base/error.html', {'error': msg})

    # else:
    #     return redirect('/file/')


def submit_load(request, *args, **kwargs):
    code = kwargs.get("code")
    BaseService.load_fight_data(code=code)
    return redirect('/service/')


def log_list(request):
    logs = WCLLog.objects.all().order_by("-id")
    return render(request, 'base/log_list.html', {'logs': logs})


def scan_viscidus_poison_tick(request, *args, **kwargs):
    log_id = kwargs.get("log_id")
    log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
    if not log_obj:
        return render(request, 'base/error.html', {'error': msg})
    scan_flag = log_obj.scan_flag
    scan_flag_dict = json.loads(scan_flag)
    if CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK in scan_flag_dict.keys():
        if scan_flag_dict.get(CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK) == 1:
            # 已经做过了小软毒箭解析，跳转日志详情页面（暂时还没做，先跳转service首页）
            return redirect('/service/')

    # 还没做过检测
    success, msg = TaqService.viscidus_poison_tick(log_id=log_id)
    if not success:
        return render(request, 'base/error.html', {'error': msg})
    scan_flag_dict[CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK] = 1
    log_obj.scan_flag = json.dumps(scan_flag_dict)
    log_obj.save()

    return redirect('/service/')


def log_detail(request, *args, **kwargs):
    log_id = kwargs.get("id")
    log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
    if not log_obj:
        return render(request, 'base/error.html', {'error': msg})

    log_detail_list, msg = BaseService.get_log_detail_list_by_id(log_id=log_id)
    content = {
        'log_detail_list': log_detail_list,
        'log_name': log_obj.title,
        'log_url': log_obj.get_wcl_link()
    }
    return render(request, 'base/log_detail.html', content)


def viscidus_poison_tick_detail(request, *args, **kwargs):
    log_id = kwargs.get("log_id")
    viscidus_poison_tick_list, msg = TaqService.get_viscidus_poison_tick_detail(log_id=log_id)
    content = {
        "viscidus_poison_tick_list": viscidus_poison_tick_list
    }
    return render(request, 'base/viscidus_poison_tick.html', content)

