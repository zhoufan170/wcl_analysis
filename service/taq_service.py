from service.api_service import WclApiService
from service.constant import CONSTANT_SERVICE
from service.base_service import BaseService
from base.models import TemplateData
from taq.models import ViscidusPoisonTick


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
                return False, msg

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
            viscidusPoisonTick_template = TemplateData(fight_id=fight.fight_id, kill=fight.kill, data=viscidusPoisonTickData)
            viscidusPoisonTick_list.append(viscidusPoisonTick_template)

        return viscidusPoisonTick_list, ''
