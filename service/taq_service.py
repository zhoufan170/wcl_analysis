from service.api_service import WclApiService
from service.constant import CONSTANT_SERVICE
from service.base_service import BaseService
from base.models import TemplateData
from taq.models import ViscidusPoisonTick, BossNatureProtection
from django.conf import settings


class TaqService():
    def __init__(self):
        pass

    @classmethod
    def viscidus_poison_tick(cls, log_id):
        log_object, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_object:
            return True, msg

        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=CONSTANT_SERVICE.Viscidus_name)
        if not fight_list or len(fight_list) == 0:
            return True, 'no viscidus fight in this log'

        for fight in fight_list:
            start = fight.start
            end = fight.end
            time = end - start
            params = {
                "start": start,
                "end": end,
                "abilityid": CONSTANT_SERVICE.Poison_Bolt_Volley_ability_id
            }

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.DAMAGE_TAKEN_VIEW,
                code=log_object.code,
                params=params
            )
            if not success:
                return False, result

            entries = result.get("entries")
            if len(entries) == 0:
                continue
                # return False, 'no poison data in log or parms error'

            for entry in entries:
                total = entry.get("total", 0)
                hitCount = entry.get("hitCount", 0)
                tickCount = entry.get("tickCount", 0)
                uptime = entry.get("uptime", 0)
                id = entry.get("id", 0)
                name = entry.get("name", "")
                viscidusPoisonTick = ViscidusPoisonTick()
                viscidusPoisonTick.fight = fight
                viscidusPoisonTick.log = log_object
                friendly, msg = BaseService.get_friendly_by_id(friendly_id=id, log_id=log_id)
                if not friendly:
                    return False, msg
                viscidusPoisonTick.friendly = friendly
                viscidusPoisonTick.name = name
                viscidusPoisonTick.damage = total
                viscidusPoisonTick.hit = hitCount
                viscidusPoisonTick.tick = tickCount
                viscidusPoisonTick.uptime = round(uptime * 100 / time, 2)
                viscidusPoisonTick.save()

        return True, ''

    @classmethod
    def get_viscidus_poison_tick_detail(cls, log_id):
        log_object, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_object:
            return None, msg

        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=CONSTANT_SERVICE.Viscidus_name)
        if not fight_list or len(fight_list) == 0:
            return None, 'no viscidus fight in this log'

        viscidusPoisonTick_list = list()
        for fight in fight_list:
            viscidusPoisonTickData = ViscidusPoisonTick.objects.filter(log=log_object, fight=fight).order_by("-tick")
            viscidusPoisonTick_template = TemplateData(fight_id=fight.fight_id, fight_name=fight.name, kill=fight.kill, data=viscidusPoisonTickData)
            viscidusPoisonTick_list.append(viscidusPoisonTick_template)

        return viscidusPoisonTick_list, ''

    @classmethod
    def get_viscidus_poison_tick_detail_api(cls, log_id):
        log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return False, '', '日志不存在'

        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=CONSTANT_SERVICE.Viscidus_name)
        if not fight_list or len(fight_list) == 0:
            return True, {}, 'no viscidus fight in this log'
        print(len(fight_list))

        viscidusPoisonTick_list = list()

        for fight in fight_list:
            tick_info_list = ViscidusPoisonTick.objects.filter(log=log_obj, fight=fight).order_by('-tick')
            tick_info_dict = dict()
            tick_info_dict['fight_id'] = fight.id
            tick_info_dict['fight_name'] = fight.name
            tick_info_dict['kill'] = fight.kill
            tick_detail_list = list()
            for tick_info in tick_info_list:
                tick_detail_dict = dict()
                tick_detail_dict['name'] = tick_info.name
                tick_detail_dict['damage'] = tick_info.damage
                tick_detail_dict['hit'] = tick_info.hit
                tick_detail_dict['tick'] = tick_info.tick
                tick_detail_dict['uptime'] = str(tick_info.uptime) + '%'
                tick_detail_list.append(tick_detail_dict)
            tick_info_dict['detail'] = tick_detail_list

            viscidusPoisonTick_list.append(tick_info_dict)

        return True, viscidusPoisonTick_list, ''

    @classmethod
    def get_boss_nature_protection_detail_api(cls, log_id):
        log_obj, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_obj:
            return False, '', '日志不存在'

        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=settings.TAQ_NATURE_PROTECTION_BOSS_LIST)
        if not fight_list or len(fight_list) == 0:
            return True, {}, 'no viscidus fight in this log'
        print(len(fight_list))

        bossNatureProtection_list = list()

        for fight in fight_list:
            nature_info_list = BossNatureProtection.objects.filter(log=log_obj, fight=fight).order_by('importance')
            nature_info_dict = dict()
            nature_info_dict['fight_id'] = fight.id
            nature_info_dict['fight_name'] = fight.name
            nature_info_dict['kill'] = fight.kill
            nature_detail_list = list()
            for nature_info in nature_info_list:
                nature_detail_dict = dict()
                nature_detail_dict['name'] = nature_info.name
                nature_detail_dict['nature_protection_absorb'] = nature_info.nature_protection_absorb
                nature_detail_dict['nature_protection_cast'] = nature_info.nature_protection_cast
                nature_detail_dict['major_nature_protection_absorb'] = nature_info.major_nature_protection_absorb
                nature_detail_dict['major_nature_protection_cast'] = nature_info.major_nature_protection_cast
                nature_detail_dict['importance'] = nature_info.importance
                nature_detail_list.append(nature_detail_dict)
            nature_info_dict['detail'] = nature_detail_list

            bossNatureProtection_list.append(nature_info_dict)

        return True, bossNatureProtection_list, ''

    @classmethod
    def nature_protection_summary(cls, log_id):
        for boss_name in settings.TAQ_NATURE_PROTECTION_BOSS_LIST:
            cls.boss_nature_protection_summary(log_id=log_id, boss_name=boss_name)
        return True, ''

    @classmethod
    def boss_nature_protection_summary(cls, log_id, boss_name):
        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=boss_name)
        if not fight_list or len(fight_list) == 0:
            return True, 'no %s fight in this log' % boss_name

        log_object, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_object:
            return False, msg

        for fight in fight_list:
            # 先获取该场boss站所有的参加人员
            success, result = WclApiService.get_api(api=CONSTANT_SERVICE.FIGHT_API, code=log_object.code, view=None, params=None)
            if not success:
                return success, result

            enemy_obj, msg = BaseService.get_enemy_by_name(log_id=log_id, name=fight.name)
            if not enemy_obj:
                continue
            fight_id_dict = {"id": fight.fight_id}
            total_result_dict = dict()
            friendlies = result.get("friendlies")
            for friendly in friendlies:
                if fight_id_dict in friendly["fights"]:
                    # this player joined the fight
                    total_result_dict[friendly["id"]] = {
                        "nature_protection_absorb": 0,
                        "nature_protection_cast": 0,
                        "nature_protection_uptime": 0.00,
                        "major_nature_protection_absorb": 0,
                        "major_nature_protection_cast": 0,
                        "major_nature_protection_uptime": 0.00,
                    }

            start = fight.start
            end = fight.end
            time = end - start

            # 小自然抗
            params = {
                "start": start,
                "end": end,
                "abilityid": CONSTANT_SERVICE.Nature_Protection_id
            }

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.HEALING_VIEW,
                code=log_object.code,
                params=params
            )

            if not success:
                return False, result

            if len(result.get("entries")) > 0:
                for entry in result.get("entries"):
                    total = entry.get("total", 0)
                    uptime = entry.get('uptime', 0)
                    friendly_id = entry.get('id', 0)
                    if friendly_id in total_result_dict.keys():
                        total_result_dict[friendly_id]["nature_protection_absorb"] = total
                        total_result_dict[friendly_id]["nature_protection_uptime"] = round(uptime * 100 / time, 2)

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.CASTS_VIEW,
                code=log_object.code,
                params=params
            )

            if not success:
                return False, result

            if len(result.get("entries")) > 0:
                for entry in result.get("entries"):
                    total = entry.get("total", 0)
                    friendly_id = entry.get('id', 0)
                    if friendly_id in total_result_dict.keys():
                        total_result_dict[friendly_id]["nature_protection_cast"] = total

            # 大自然抗
            params = {
                "start": start,
                "end": end,
                "abilityid": CONSTANT_SERVICE.Major_Nature_Protection_id
            }

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.HEALING_VIEW,
                code=log_object.code,
                params=params
            )

            if not success:
                return False, result

            if len(result.get("entries")) > 0:
                for entry in result.get("entries"):
                    total = entry.get("total", 0)
                    uptime = entry.get('uptime', 0)
                    friendly_id = entry.get('id', 0)
                    if friendly_id in total_result_dict.keys():
                        total_result_dict[friendly_id]["major_nature_protection_absorb"] = total
                        total_result_dict[friendly_id]["major_nature_protection_uptime"] = round(uptime * 100 / time, 2)

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.CASTS_VIEW,
                code=log_object.code,
                params=params
            )

            if not success:
                return False, result

            if len(result.get("entries")) > 0:
                for entry in result.get("entries"):
                    total = entry.get("total")
                    friendly_id = entry.get('id')
                    if friendly_id in total_result_dict.keys():
                        total_result_dict[friendly_id]["major_nature_protection_cast"] = total

            # import json
            # print(json.dumps(total_result_dict))
            for key, value in total_result_dict.items():
                friendly_obj, msg = BaseService.get_friendly_by_id(friendly_id=key, log_id=log_id)
                if not friendly_obj:
                    continue
                bossNatureProtection = BossNatureProtection()
                bossNatureProtection.friendly = friendly_obj
                bossNatureProtection.log = log_object
                bossNatureProtection.fight = fight
                bossNatureProtection.enemy = enemy_obj
                bossNatureProtection.name = friendly_obj.name
                bossNatureProtection.nature_protection_absorb = value.get("nature_protection_absorb", 0)
                bossNatureProtection.nature_protection_cast = value.get("nature_protection_cast", 0)
                bossNatureProtection.nature_protection_uptime = value.get("nature_protection_uptime", 0)
                bossNatureProtection.major_nature_protection_absorb = value.get("major_nature_protection_absorb", 0)
                bossNatureProtection.major_nature_protection_cast = value.get("major_nature_protection_cast", 0)
                bossNatureProtection.major_nature_protection_uptime = value.get("major_nature_protection_uptime", 0)
                if boss_name == CONSTANT_SERVICE.Hururan_name:
                    if friendly_obj.is_melee():
                        # melee
                        if bossNatureProtection.nature_protection_absorb > 0 and bossNatureProtection.major_nature_protection_cast == 0:
                            bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L1
                        elif bossNatureProtection.nature_protection_absorb > 0 or bossNatureProtection.major_nature_protection_cast == 0:
                            bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L2
                        else:
                            bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L3
                    else:
                        if bossNatureProtection.nature_protection_absorb > 0:
                            bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L1
                        else:
                            bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L3
                else:
                    if bossNatureProtection.nature_protection_absorb > 0:
                        bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L1
                    else:
                        bossNatureProtection.importance = BossNatureProtection.IMPORTANCE_L3

                bossNatureProtection.save()

        return True, ''

    @classmethod
    def get_boss_nature_protection_detail(cls, log_id):
        log_object, msg = BaseService.get_wcl_log_by_id(log_id=log_id)
        if not log_object:
            return None, msg

        fight_list, msg = BaseService.get_fight_list(log_id=log_id, name=settings.TAQ_NATURE_PROTECTION_BOSS_LIST)
        if not fight_list or len(fight_list) == 0:
            return None, 'no relation fight in this log'

        bossNatureProtection_list = list()
        for fight in fight_list:
            bossNatureProtectionData = BossNatureProtection.objects.filter(log=log_object, fight=fight).order_by("importance")
            bossNatureProtection_template = TemplateData(fight_id=fight.fight_id, fight_name=fight.name,
                                                         kill=fight.kill,
                                                         data=bossNatureProtectionData)
            bossNatureProtection_list.append(bossNatureProtection_template)

        return bossNatureProtection_list, ''