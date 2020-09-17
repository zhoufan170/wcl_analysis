from django.core.management.base import BaseCommand, CommandError
from base.models import WCLLog, Friendly, Enemy, Fight
from django.conf import settings
from service.constant import CONSTANT_SERVICE
import configparser
from service.base_service import BaseService
from service.api_service import WclApiService
from taq.models import TaqGoldRunDetail


class Command(BaseCommand):
    help = 'C帝金团分金工具'

    def handle(self, *args, **options):
        golden_config_file = '/home/wcl/C帝分金配置.txt'
        conf = configparser.ConfigParser()
        conf.read(golden_config_file)
        code = conf['log']['code']
        log_obj, msg = BaseService.get_wcl_log_by_code(code=code)
        if not log_obj:
            print('日志code错误或未登记')
            return

        # 每次运行任务，重新生成一次数据，把以前的数据清理掉
        taq_run_detail_list = TaqGoldRunDetail.objects.filter(log=log_obj)
        if len(taq_run_detail_list) > 0:
            for taq_run_detail in taq_run_detail_list:
                taq_run_detail.reset()
        else:
            friendlies, msg = BaseService.get_all_friendly_by_log(log_id=log_obj.id)
            for friendly in friendlies:
                taqGoldRunDetail = TaqGoldRunDetail()
                taqGoldRunDetail.log = log_obj
                taqGoldRunDetail.name = friendly.name
                taqGoldRunDetail.classic = friendly.type
                taqGoldRunDetail.save()

        tank_list = (conf['tank']['tank_list']).split('|')
        punishment = conf['punishment']

        jumper = conf['jumper']['jumper']
        hunter = conf['jumper']['hunter']

        success, result = self.tank(tank_list=tank_list, log_obj=log_obj)
        if not success:
            print(result)
            return

        success, result = self.heal(log_obj=log_obj)
        if not success:
            print(result)
            return

        success, result = self.dps(log_obj=log_obj, jumper=jumper, hunter=hunter)
        if not success:
            print(result)
            return

        success, result = self.punishment(log_obj=log_obj, punishment_detail=punishment)
        if not success:
            print(result)
            return

        success, result = self.total_caculator(log_obj=log_obj, total=int(conf['log']['total']) - 200) # 扣除在下200金技术补贴
        if not success:
            print(result)
            return

        print('%s/service/gold_run_detail/%s' % (settings.SELF_SCHEMA, str(log_obj.id)))

    def tank(self, tank_list, log_obj):
        tank_dict = dict()
        for tank in tank_list:
            tank_dict[tank] = 0

        # 计算全程，各坦克的active(uptime)
        all_fight_list = Fight.objects.filter(log=log_obj).order_by('fight_id')
        if len(all_fight_list) == 0:
            return False, '该日志无有效的战斗记录'

        start = 0
        end = all_fight_list[len(all_fight_list) - 1].end
        params = {
            'start': start,
            'end': end
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_TAKEN_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get("entries")
        if len(entries) == 0:
            return False, '承受伤害无有效记录'

        for tank in tank_list:
            for entry in entries:
                if tank == entry.get("name"):
                    tank_dict[tank] = entry.get("activeTime")

        # 再去除掉无效的战斗
        unavailable_fights = Fight.objects.filter(log=log_obj, name__in=CONSTANT_SERVICE.TAQ_UNAVAILABLE_TRASH_NAME)
        if len(unavailable_fights) > 0:
            for fight in unavailable_fights:
                params = {
                    'start': fight.start,
                    'end': fight.end
                }

                success, result = WclApiService.get_api(
                    api=CONSTANT_SERVICE.TABLES_API,
                    view=CONSTANT_SERVICE.DAMAGE_TAKEN_VIEW,
                    code=log_obj.code,
                    params=params
                )
                if not success:
                    return False, result

                entries = result.get("entries")
                if len(entries) == 0:
                    continue

                for tank in tank_list:
                    for entry in entries:
                        if tank == entry.get("name"):
                            tank_dict[tank] = tank_dict[tank] - entry.get("activeTime")

        # 算active总和
        total_active = 0
        for key, value in tank_dict.items():
            total_active = total_active + tank_dict[key]

        for key, value in tank_dict.items():
            tank = round((tank_dict[key]/total_active) * 1200)
            run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=key).first()
            run_obj.tank = run_obj.tank + tank
            run_obj.tag = 'tank'
            run_obj.save()

        # 默认active前2的坦克补贴泰坦
        titan_dict = dict()

        sort_list = sorted(tank_dict.items(), key=lambda d: d[1], reverse=True)
        titan_dict[sort_list[0][0]] = 250
        titan_dict[sort_list[1][0]] = 250
        for key, value in titan_dict.items():
            run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=key).first()
            run_obj.titan = run_obj.titan + value
            run_obj.tag = 'tank'
            run_obj.save()

        # 再找2个sst
        twins_fight = Fight.objects.filter(log=log_obj, name=CONSTANT_SERVICE.Twins_name, kill=True).first()
        params = {
            'start': twins_fight.start,
            'end': twins_fight.end
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_TAKEN_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get("entries")
        if len(entries) == 0:
            return False, '双子战斗没有数据'

        warlock_dict = dict()
        for entry in entries:
            if entry.get('type') == 'Warlock':
                warlock_dict[entry.get('name')] = entry.get('total')

        # print(warlock_dict)
        sort_list = sorted(warlock_dict.items(), key=lambda d: d[1], reverse=True)

        tank_dict[sort_list[0][0]] = 150
        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[0][0], sort_list[1][0]])
        for run_obj in run_obj_list:
            run_obj.tag = 'range'
            run_obj.tank = run_obj.tank + 150
            run_obj.save()

        # 奥罗撒币哥
        ouro_fight = Fight.objects.filter(log=log_obj, name=CONSTANT_SERVICE.Ouro_name, kill=True).first()
        params = {
            'start': ouro_fight.start,
            'end': ouro_fight.end,
            'abilityid': CONSTANT_SERVICE.Greater_Blessing_Of_Kings
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.CASTS_VIEW,
            code=log_obj.code,
            params=params
        )

        entries = result.get("entries")
        if len(entries) == 0:
            return False, '奥罗战斗没有数据'

        paladin_dict = dict()
        for entry in entries:
            if entry.get('type') == 'Paladin':
                paladin_dict[entry.get('name')] = entry.get('total')

        sort_list = sorted(paladin_dict.items(), key=lambda d: d[1], reverse=True)

        run_obj = TaqGoldRunDetail.objects.filter(name=sort_list[0][0], log=log_obj).first()
        if run_obj:
            run_obj.tag = 'heal'
            run_obj.tank = run_obj.tank + 100
            run_obj.save()

        return True, ''

    def heal(self, log_obj):
        # 先计算全程治疗
        all_fight_list = Fight.objects.filter(log=log_obj).order_by('fight_id')
        if len(all_fight_list) == 0:
            return False, '该日志无有效的战斗记录'

        start = 0
        end = all_fight_list[len(all_fight_list) - 1].end
        params = {
            'start': start,
            'end': end
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.HEALING_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        all_healing_dict = dict()
        paladin_healing_dict = dict()
        priest_healing_dict = dict()
        druid_healing_dict = dict()
        entries = result.get('entries')

        if len(entries) == 0:
            return False, '没有有效的全程治疗数据'

        for entry in entries:
            if entry.get('total') > 200000:
                all_healing_dict[entry.get('name')] = entry.get('total')
                if entry.get('type') == 'Paladin':
                    paladin_healing_dict[entry.get('name')] = entry.get('total')
                elif entry.get('type') == 'Priest':
                    priest_healing_dict[entry.get('name')] = entry.get('total')
                elif entry.get('type') == 'Druid':
                    druid_healing_dict[entry.get('name')] = entry.get('total')

        # 先给全程超过20万的治疗打标
        heal_run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=all_healing_dict.keys())
        for run_obj in heal_run_obj_list:
            run_obj.tag = 'heal'
            run_obj.save()

        # 先算全程前5
        sort_list = sorted(all_healing_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.tag = 'heal'
        run_obj.heal_total = run_obj.heal_total + 200
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.tag = 'heal'
            run_obj.heal_total = run_obj.heal_total + 100
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.tag = 'heal'
            run_obj.heal_total = run_obj.heal_total + 50
            run_obj.save()

        # 骑士第一
        sort_list = sorted(paladin_healing_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.tag = 'heal'
        run_obj.heal_classic = run_obj.heal_classic + 50
        run_obj.save()

        # 牧师第一
        sort_list = sorted(priest_healing_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.tag = 'heal'
        run_obj.heal_classic = run_obj.heal_classic + 50
        run_obj.save()

        # 小德第一
        sort_list = sorted(druid_healing_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.tag = 'heal'
        run_obj.heal_classic = run_obj.heal_classic + 50
        run_obj.save()

        # boss战斗治疗
        boss_fight_list = Fight.objects.filter(log=log_obj, boss__gt=1)
        boss_heal_dict = dict()
        for boss_fight in boss_fight_list:
            params = {
                "start": boss_fight.start,
                "end": boss_fight.end
            }

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.HEALING_VIEW,
                code=log_obj.code,
                params=params
            )

            if not success:
                return False, result

            entries = result.get('entries')
            if len(entries) == 0:
                continue

            for entry in entries:
                if entry.get("name") in all_healing_dict.keys():
                    if entry.get("name") in boss_heal_dict.keys():
                        boss_heal_dict[entry.get("name")] = boss_heal_dict[entry.get("name")] + entry.get('total')
                    else:
                        boss_heal_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(boss_heal_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.tag = 'heal'
        run_obj.heal_boss = run_obj.heal_boss + 100
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.tag = 'heal'
            run_obj.heal_boss = run_obj.heal_boss + 50
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.tag = 'heal'
            run_obj.heal_boss = run_obj.heal_boss + 25
            run_obj.save()

        # 驱散
        params = {
            "start": start,
            "end": end
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DISPELS_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        all_dispel_dict = dict()
        entries = result.get('entries')
        for entry in entries:
            second_entries = entry.get('entries')
            for second_entry in second_entries:
                # list里每一项是一个debuff的驱散数据
                details = second_entry.get("details")
                if not details:
                    continue
                if len(details) == 0:
                    continue

                for detail in details:
                    if detail.get("name") in all_dispel_dict.keys():
                        all_dispel_dict[detail.get("name")] = all_dispel_dict[detail.get("name")] + detail.get('total')
                    else:
                        all_dispel_dict[detail.get("name")] = detail.get('total')

        sort_list = sorted(all_dispel_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dispel = run_obj.dispel + 100
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dispel = run_obj.dispel + 50
            run_obj.save()

        return True, ''

    def dps(self, log_obj, jumper, hunter):
        # 先打标
        all_fight_list = Fight.objects.filter(log=log_obj).order_by('fight_id')
        if len(all_fight_list) == 0:
            return False, '该日志无有效的战斗记录'

        start = 0
        end = all_fight_list[len(all_fight_list) - 1].end

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, tag='')
        for run_obj in run_obj_list:
            if run_obj.classic in ['Warrior', 'Paladin', 'Rogue']:
                run_obj.tag = 'melee'
            elif run_obj.classic in ['Hunter', 'Mage', 'Priest', 'Warlock']:
                run_obj.tag = 'range'
            else:
                # 小德特殊处理，查平砍伤害，超过10万定义为近战
                friendly = Friendly.objects.filter(name=run_obj.name, log=log_obj).first()
                if not friendly:
                    continue
                params = {
                    'start': start,
                    'end': end,
                    'abilityid': CONSTANT_SERVICE.Melee,
                    'sourceid': friendly.friendly_id
                }

                success, result = WclApiService.get_api(
                    api=CONSTANT_SERVICE.TABLES_API,
                    view=CONSTANT_SERVICE.DAMAGE_VIEW,
                    code=log_obj.code,
                    params=params
                )
                if not success:
                    continue

                total_melee = 0
                entries = result.get('entries')
                for entry in entries:
                    total_melee = total_melee + entry.get('total')

                if total_melee > 100000:
                    run_obj.tag = 'melee'
                else:
                    run_obj.tag = 'range'

            run_obj.save()

        # 全程dps
        total_dps_dict = dict()
        total_melee_dict = dict()
        total_range_dict = dict()

        params = {
            'start': start,
            'end': end,
        }
        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_VIEW,
            code=log_obj.code,
            params=params
        )
        if not success:
            return False, result

        entries = result.get('entries')
        for entry in entries:
            run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=entry.get('name')).first()
            if run_obj.tag == 'melee':
                total_dps_dict[entry.get('name')] = entry.get('total')
                total_melee_dict[entry.get('name')] = entry.get('total')
            elif run_obj.tag == 'range':
                total_dps_dict[entry.get('name')] = entry.get('total')
                total_range_dict[entry.get('name')] = entry.get('total')
            else:
                continue

        # 近战前5
        sort_list = sorted(total_melee_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_total_melee = run_obj.dps_total_melee + 200
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_total_melee = run_obj.dps_total_melee + 100
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.dps_total_melee = run_obj.dps_total_melee + 50
            run_obj.save()

        # 远程前5
        sort_list = sorted(total_range_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_total_range = run_obj.dps_total_range + 200
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_total_range = run_obj.dps_total_range + 100
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.dps_total_range = run_obj.dps_total_range + 50
            run_obj.save()

        # 倒数前5罚款
        sort_list = sorted(total_range_dict.items(), key=lambda d: d[1])
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_punishment = run_obj.dps_punishment - 100
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_punishment = run_obj.dps_punishment - 50
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.dps_punishment = run_obj.dps_punishment -25
            run_obj.save()

        # boss dps
        boss_fight_list = Fight.objects.filter(log=log_obj, boss__gt=1)
        boss_dps_dict = dict()
        for boss_fight in boss_fight_list:
            params = {
                "start": boss_fight.start,
                "end": boss_fight.end
            }

            success, result = WclApiService.get_api(
                api=CONSTANT_SERVICE.TABLES_API,
                view=CONSTANT_SERVICE.DAMAGE_VIEW,
                code=log_obj.code,
                params=params
            )

            if not success:
                return False, result

            entries = result.get('entries')
            if len(entries) == 0:
                continue

            for entry in entries:
                if entry.get("name") in total_dps_dict.keys():
                    if entry.get("name") in boss_dps_dict.keys():
                        boss_dps_dict[entry.get("name")] = boss_dps_dict[entry.get("name")] + entry.get('total')
                    else:
                        boss_dps_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(boss_dps_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_boss = run_obj.dps_boss + 100
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_boss = run_obj.dps_boss + 50
            run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[3][0], sort_list[4][0]])
        for run_obj in run_obj_list:
            run_obj.dps_boss = run_obj.dps_boss + 25
            run_obj.save()

        # 判断是否跳怪
        if jumper == '1':
            run_obj = TaqGoldRunDetail.objects.filter(name=hunter, log=log_obj).first()
            if run_obj:
                run_obj.jumper = run_obj.jumper + 100
                run_obj.save()
            return True, ''

        # 不跳怪，计算天堂路几个怪的dps
        # 其拉勇士
        qira_champion_dict = dict()
        enemy_obj = Enemy.objects.filter(log=log_obj, name='其拉勇士').first()
        if not enemy_obj:
            return False, '没有有效的其拉勇士战斗数据'

        params = {
            "start": start,
            "end": end,
            "targetid": enemy_obj.enemy_id
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get('entries')
        if len(entries) == 0:
            return False, '没有有效的其拉勇士战斗数据'

        for entry in entries:
            qira_champion_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(qira_champion_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_qiraji_champion = run_obj.dps_qiraji_champion + 50
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_qiraji_champion = run_obj.dps_qiraji_champion + 25
            run_obj.save()

        # 其拉执行者
        qira_slayer_dict = dict()
        enemy_obj = Enemy.objects.filter(log=log_obj, name='其拉执行者').first()
        if not enemy_obj:
            return False, '没有有效的其拉执行者战斗数据'

        params = {
            "start": start,
            "end": end,
            "targetid": enemy_obj.enemy_id
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get('entries')
        if len(entries) == 0:
            return False, '没有有效的其拉执行者战斗数据'

        for entry in entries:
            qira_slayer_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(qira_slayer_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_qiraji_slayer = run_obj.dps_qiraji_slayer + 100
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_qiraji_slayer = run_obj.dps_qiraji_slayer + 50
            run_obj.save()

        # 其拉斩灵者
        qira_mindslayer_dict = dict()
        enemy_obj = Enemy.objects.filter(log=log_obj, name='其拉斩灵者').first()
        if not enemy_obj:
            return False, '没有有效的其拉斩灵者战斗数据'

        params = {
            "start": start,
            "end": end,
            "targetid": enemy_obj.enemy_id
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get('entries')
        if len(entries) == 0:
            return False, '没有有效的其拉斩灵者战斗数据'

        for entry in entries:
            qira_mindslayer_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(qira_mindslayer_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_qiraji_mindslayer = run_obj.dps_qiraji_mindslayer + 50
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_qiraji_mindslayer = run_obj.dps_qiraji_mindslayer + 25
            run_obj.save()

        # 黑曜石终结者
        obsidian_nullifier_dict = dict()
        enemy_obj = Enemy.objects.filter(log=log_obj, name='黑曜石终结者').first()
        if not enemy_obj:
            return False, '没有有效的黑曜石终结者战斗数据'

        params = {
            "start": start,
            "end": end,
            "targetid": enemy_obj.enemy_id
        }

        success, result = WclApiService.get_api(
            api=CONSTANT_SERVICE.TABLES_API,
            view=CONSTANT_SERVICE.DAMAGE_VIEW,
            code=log_obj.code,
            params=params
        )

        if not success:
            return False, result

        entries = result.get('entries')
        if len(entries) == 0:
            return False, '没有有效的黑曜石终结者战斗数据'

        for entry in entries:
            obsidian_nullifier_dict[entry.get("name")] = entry.get('total')

        sort_list = sorted(obsidian_nullifier_dict.items(), key=lambda d: d[1], reverse=True)
        run_obj = TaqGoldRunDetail.objects.filter(log=log_obj, name=sort_list[0][0]).first()
        run_obj.dps_obsidian_nullifier = run_obj.dps_obsidian_nullifier + 50
        run_obj.save()

        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj, name__in=[sort_list[1][0], sort_list[2][0]])
        for run_obj in run_obj_list:
            run_obj.dps_obsidian_nullifier = run_obj.dps_obsidian_nullifier + 25
            run_obj.save()

        return True, ''

    def punishment(self, log_obj, punishment_detail):
        for key in punishment_detail:
            run_obj = TaqGoldRunDetail.objects.filter(name__iexact=key, log=log_obj).first()
            if run_obj:
                run_obj.other_punishment = run_obj.other_punishment - int(punishment_detail[key])
                run_obj.save()

        return True, ''

    def total_caculator(self, log_obj, total):
        run_obj_list = TaqGoldRunDetail.objects.filter(log=log_obj)
        count = len(run_obj_list)
        total_fee = 0
        for run_obj in run_obj_list:
            total_fee = total_fee + run_obj.all_fee()

        base = round((total - total_fee) / count)

        for run_obj in run_obj_list:
            run_obj.base_gold = base
            run_obj.total_gold = base + run_obj.all_fee()
            run_obj.save()

        return True, ''