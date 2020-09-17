from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from base.form import LoadReportForm
from service.base_service import BaseService
from base.models import WCLLog, GoldRunTemplateData
from service.constant import CONSTANT_SERVICE
import json
from service.taq_service import TaqService
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wcl_analysis.tasks import viscidus_poison_tick_task, boss_nature_protection_task
from taq.models import TaqGoldRunDetail

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
    paginator = Paginator(logs, 10)
    page = request.GET.get('page', 1)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'base/log_list.html', {'logs': contacts})


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

    BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK, flag=-1)
    # 还没做过检测
    # success, msg = TaqService.viscidus_poison_tick(log_id=log_id)
    # TaqService.viscidus_poison_tick.apply_async(args=[log_id])
    viscidus_poison_tick_task.apply_async(args=[log_id], queue='wcl_analysis')
    # scan_flag_dict[CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK] = 1
    # log_obj.scan_flag = json.dumps(scan_flag_dict)
    # log_obj.save()

    # return redirect('%s' % str(log_id))
    return HttpResponseRedirect(reverse('base:log_detail', kwargs={"id": log_id}))
    # return reverse(viewname=log_detail, kwargs={"id": log_id})


def log_detail(request, *args, **kwargs):
    log_id = kwargs.get("id")
    log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
    if not log_obj:
        return render(request, 'base/error.html', {'error': msg})

    log_detail_list, msg = BaseService.get_log_detail_list_by_id(log_id=log_id)
    content = {
        'log_id': log_id,
        'log_detail_list': log_detail_list,
        'log_name': log_obj.title,
        'log_url': log_obj.get_wcl_link()
    }
    return render(request, 'base/log_detail.html', content)


def viscidus_poison_tick_info(request, *args, **kwargs):
    log_id = kwargs.get("log_id")
    viscidus_poison_tick_list, msg = TaqService.get_viscidus_poison_tick_detail(log_id=log_id)
    content = {
        "viscidus_poison_tick_list": viscidus_poison_tick_list
    }
    return render(request, 'base/viscidus_poison_tick.html', content)


def scan_boss_nature_protection(request, *args, **kwargs):
    log_id = kwargs.get("log_id")
    log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
    if not log_obj:
        return render(request, 'base/error.html', {'error': msg})
    scan_flag = log_obj.scan_flag
    scan_flag_dict = json.loads(scan_flag)
    if CONSTANT_SERVICE.BOSS_NATURE_PROTECTION in scan_flag_dict.keys():
        if scan_flag_dict.get(CONSTANT_SERVICE.BOSS_NATURE_PROTECTION) == 1:
            # 已经做过了boss战自然抗检测，跳转日志详情页面（暂时还没做，先跳转service首页）
            return redirect('/service/')

    BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.BOSS_NATURE_PROTECTION, flag=-1)
    # 还没做过检测
    # success, msg = TaqService.nature_protection_summary(log_id=log_id)
    # if not success:
    #     return render(request, 'base/error.html', {'error': msg})
    boss_nature_protection_task.apply_async(args=[log_id], queue='wcl_analysis')
    # scan_flag_dict[CONSTANT_SERVICE.BOSS_NATURE_PROTECTION] = 1
    # log_obj.scan_flag = json.dumps(scan_flag_dict)
    # log_obj.save()

    return HttpResponseRedirect(reverse('base:log_detail', kwargs={"id": log_id}))


def boss_nature_protection_info(request, *args, **kwargs):
    log_id = kwargs.get("log_id")
    boss_nature_protection_list, msg = TaqService.get_boss_nature_protection_detail(log_id=log_id)
    content = {
        "boss_nature_protection_list": boss_nature_protection_list
    }
    return render(request, 'base/boss_nature_protection.html', content)


def gold_run_detail(request, *args, **kwargs):
    log_id = kwargs.get("id")
    log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
    if not log_obj:
        return render(request, 'base/error.html', {'error': msg})

    run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj).order_by('-tag')
    if len(run_obj_list) < 1:
        return render(request, 'base/error.html', {'error': '没有分金明细数据'})

    gold_run_data = GoldRunTemplateData(log=log_obj, run_obj_list=run_obj_list)
    content = {
        "gold_run_data": gold_run_data
    }

    return render(request, 'base/gold_run_detail.html', content)


