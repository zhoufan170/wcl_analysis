from service.api_service import WclApiService
from service.constant import CONSTANT_SERVICE
from base.models import WCLLog, Fight, Friendly, Enemy, LogDetail
from django.conf import settings
import json
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
# 这里没有引用的"wcl_analysis.tasks"不能注释掉,因为调用celery任务用到exec(func_str)，func_str里有这个引用
import wcl_analysis.tasks


class BaseService():
    def __init__(self):
        pass

    @classmethod
    def load_fight_data(cls, code, raid):
        """
        加载日志，fight数据
        :param code:
        :return:
        """
        if len(WCLLog.objects.filter(code=code)) > 0:
            return False, '您的日志已登记，请勿重复登记'

        success, result = WclApiService.get_api(api=CONSTANT_SERVICE.FIGHT_API, code=code, view=None, params=None)
        if not success:
            return success, result

        wcl_log = WCLLog()
        wcl_log.title = result.get("title", "")
        wcl_log.code = code
        wcl_log.raid = raid
        wcl_log.owner = result.get("owner", "")
        wcl_log.start = result.get("start", 0)
        wcl_log.end = result.get("end", 0)
        wcl_log.zone = result.get("zone", "")
        wcl_log.parse_flag = False
        wcl_log.save()

        fights = result.get('fights')
        if len(fights) > 0:
            for fight_data in fights:
                fight = Fight()
                fight.log = wcl_log
                fight.fight_id = fight_data.get("id", 0)
                fight.start = fight_data.get("start_time", 0)
                fight.end = fight_data.get("end_time", 0)
                fight.boss = fight_data.get("boss", 0)
                fight.kill = fight_data.get("kill", True)
                fight.name = fight_data.get("name", "")
                fight.save()

        friendlies = result.get('friendlies')
        if len(friendlies) > 0:
            for friendly_data in friendlies:
                friendly = Friendly()
                friendly.log = wcl_log
                friendly.name = friendly_data.get("name", "")
                friendly.friendly_id = friendly_data.get("id", 0)
                friendly.guid = friendly_data.get("guid", 0)
                friendly.type = friendly_data.get("type", "")
                friendly.server = friendly_data.get("server", "")
                friendly.save()

        enemies = result.get("enemies")
        if len(enemies) > 0:
            for enemy_data in enemies:
                enemy = Enemy()
                enemy.log = wcl_log
                enemy.name = enemy_data.get("name", "")
                enemy.enemy_id = enemy_data.get("id", 0)
                enemy.guid = enemy_data.get("guid", 0)
                enemy.type = enemy_data.get("type", "")
                enemy.save()

        return True, ''

    @classmethod
    def get_wcl_log_by_id(cls, log_id):
        '''
        根据log id获取日志对象
        :param log_id:
        :return:
        '''
        if not log_id or log_id == 0:
            return None, 'log id is none or 0'

        log_object = WCLLog.objects.filter(id=log_id)
        if not log_object:
            return None, 'wcl log not exist'

        return log_object.first(), ''

    @classmethod
    def get_wcl_log_by_code(cls, code):
        '''
        根据code获取日志对象
        :param code:
        :return:
        '''
        if not code or code == '':
            return None, 'code is none'

        log_object = WCLLog.objects.filter(code=code)
        if not log_object:
            return None, 'wcl log not exist'

        return log_object.first(), ''

    @classmethod
    def get_fight_list(cls, log_id, name):
        '''
        根据boss查找战斗列表
        :param log_id:
        :param name:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg
        if isinstance(name, list):
            fight_list = Fight.objects.filter(log=log_obj, name__in=name, boss__gt=0)
        else:
            fight_list = Fight.objects.filter(log=log_obj, name=name, boss__gt=0)
        return fight_list, ''

    @classmethod
    def get_friendly_by_id(cls, friendly_id, log_id):
        '''
        根据id查找友方目标
        :param friendly_id:
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        friendly_obj = Friendly.objects.filter(friendly_id=friendly_id, log=log_obj).first()
        if not friendly_obj:
            print(friendly_id, log_obj.id)
            return None, 'friendly not exist'

        return friendly_obj, ''

    @classmethod
    def get_all_friendly_by_log(cls, log_id):
        '''
        查找一个日志中所有友方目标
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        friendly_obj = Friendly.objects.filter(log=log_obj)
        return friendly_obj, ''

    @classmethod
    def get_log_detail_list_by_id(cls, log_id):
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        log_detail_list = list()
        for detail in settings.TAQ_DETAIL_LIST:
            detail_type = detail[0]
            detail_name = detail[1]
            detail_scan_url = detail[2]
            detail_info_url = detail[3]
            scan_flag_dict = json.loads(log_obj.scan_flag)
            if detail_type in scan_flag_dict.keys():
                # if scan_flag_dict[detail_type] == 1:
                #     scan_flag = True
                # else:
                #     scan_flag = False
                scan_flag = scan_flag_dict[detail_type]
            else:
                scan_flag = 0
            log_detail = LogDetail(detail_type=detail_type,
                                   detail_name=detail_name,
                                   detail_scan_url='/service%s%s' % (detail_scan_url, str(log_id)),
                                   detail_info_url='/service%s%s' % (detail_info_url, str(log_id)),
                                   scan_flag=scan_flag)
            log_detail_list.append(log_detail)

        return log_detail_list, ''

    @classmethod
    def get_log_detail_list_by_id_for_api(cls, log_id):
        '''
        用于新版api
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        if log_obj.raid == 'TAQ':
            detail_list = settings.TAQ_DETAIL_LIST
        elif log_obj.raid == 'NAXX':
            detail_list = settings.NAXX_DETAIL_LIST
        else:
            return None, '暂时不支持%s' % log_obj.raid

        log_detail_list = list()
        for detail in detail_list:
            detail_type = detail[0]
            detail_name = detail[1]
            scan_flag_dict = json.loads(log_obj.scan_flag)
            if detail_type in scan_flag_dict.keys():
                # if scan_flag_dict[detail_type] == 1:
                #     scan_flag = True
                # else:
                #     scan_flag = False
                scan_flag = scan_flag_dict[detail_type]
            else:
                scan_flag = 0

            log_detail_list.append({
                "type": detail_type,
                "name": detail_name,
                "scan_flag": scan_flag
            })

        return {"scan_list": log_detail_list, "raid": log_obj.raid, "code": log_obj.code,
                "owner": log_obj.owner, "start": log_obj.start, "end": log_obj.end, "zone": log_obj.zone,
                "upload_time": log_obj.format_upload_time(), "total": log_obj.total_time(),
                "wcl_link": log_obj.get_wcl_link(), "title": log_obj.title}, ''

    @classmethod
    def get_enemy_by_name(cls, log_id, name):
        '''
        根据name查找敌对目标
        :param log_id:
        :param name:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return None, msg

        enemy_obj = Enemy.objects.filter(log=log_obj, name=name).first()
        if not enemy_obj:
            return None, 'enemy: %s not exist' % name

        return enemy_obj, ''

    @classmethod
    def test_task_async(cls):
        from wcl_analysis.tasks import test_task
        print("begin to call task")
        test_task.apply_async(args=[], queue='wcl_analysis')
        # test_task.delay()
        print("end to call task")

    @classmethod
    def update_sync_flag(cls, log_id, task, flag):
        '''
        更新扫描任务处理状态
        :param log_id:
        :return:
        '''
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return False, msg

        scan_flag = json.loads(log_obj.scan_flag)
        scan_flag[task] = flag
        log_obj.scan_flag = json.dumps(scan_flag)
        log_obj.save()
        return True, ''

    @classmethod
    def get_log_list(cls, raid, code, page, per_page):
        if raid and code:
            query_params = Q(raid=raid) & Q(code=code)
        elif raid or code:
            if raid:
                query_params = Q(raid=raid)
            else:
                query_params = Q(code=code)
        else:
            query_params = None

        if query_params:
            log_list = WCLLog.objects.filter(query_params).order_by('-id')
        else:
            log_list = WCLLog.objects.all().order_by('-id')

        paginator = Paginator(log_list, per_page)

        try:
            wcl_log_paginator = paginator.page(page)
        except PageNotAnInteger:
            wcl_log_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            wcl_log_paginator = paginator.page(paginator.num_pages)

        wcl_log_list = wcl_log_paginator.object_list
        wcl_log_restful_list = []
        for wcl_log in wcl_log_list:
            wcl_log_restful_list.append(dict(id=wcl_log.id,
                                             title=wcl_log.title,
                                             code=wcl_log.code,
                                             raid=wcl_log.raid,
                                             owner=wcl_log.owner,
                                             start=wcl_log.start,
                                             end=wcl_log.end,
                                             zone=wcl_log.zone,
                                             parse_flag=wcl_log.parse_flag,
                                             upload_time=wcl_log.format_upload_time(),
                                             scan_flag=wcl_log.scan_flag,
                                             total=wcl_log.total_time(),
                                             date=time.strftime('%Y-%m-%d', time.localtime(int(wcl_log.start / 1000))))
                                        )

        return wcl_log_restful_list, dict(per_page=int(per_page),
                                          page=int(page) if int(page) <= paginator.count else paginator.count,
                                          total=paginator.count)

    @classmethod
    def run_all_scan_task(cls, log_id):
        log_obj, msg = cls.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return False, msg

        scan_flag_dict = json.loads(log_obj.scan_flag)
        if log_obj.raid == 'TAQ':
            task_list = settings.TAQ_DETAIL_LIST
        elif log_obj.raid == 'NAXX':
            task_list = settings.NAXX_DETAIL_LIST
        else:
            return False, '暂时不支持%s' % log_obj.raid

        for task in task_list:
            if task[0] not in scan_flag_dict.keys() or scan_flag_dict.get(task[0]) != 1:
                # 任务未运行
                cls.run_single_task(log_id=log_id, task_name=task[0])
            else:
                continue

        return True, ''

    @classmethod
    def run_single_task(cls, log_id, task_name):
        BaseService.update_sync_flag(log_id=log_id, task=task_name, flag=-1)
        func_str = "wcl_analysis.tasks.%s_task.apply_async(args=[%s], queue='wcl_analysis')" % (task_name, str(log_id))
        exec(func_str)
