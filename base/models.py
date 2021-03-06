from django.db import models
import datetime

# Create your models here.


class WCLLog(models.Model):
    title = models.CharField(default="wcl log", max_length=100, verbose_name="标题")
    code = models.CharField(default="wcl_code", unique=True, max_length=50, verbose_name="wcl report code")
    owner = models.CharField(default="xlinna", max_length=50, verbose_name="owner")
    raid = models.CharField(default='TAQ', max_length=50, verbose_name='副本')
    start = models.IntegerField(default=0, verbose_name="开始时间（timestamp毫秒）")
    end = models.IntegerField(default=0, verbose_name="结束时间（timestamp毫秒）")
    zone = models.IntegerField(default=0, verbose_name="区域")
    parse_flag = models.BooleanField(default=False, verbose_name="日志解析状态")
    upload_time = models.DateTimeField(default=datetime.datetime.now())
    scan_flag = models.CharField(max_length=1000, default='{}')

    def total_time(self):
        seconds_total = int((self.end - self.start) / 1000)
        # hours = int(seconds_total / 3600)
        # minutes = int((seconds_total - 3600 * hours) / 60)
        # seconds = int((seconds_total - 3600 * hours) % 60)
        # return '%d:%d:%d' % (hours, minutes, seconds)
        h, m = divmod(seconds_total, 3600)
        m, s = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def format_upload_time(self):
        return (self.upload_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

    def get_wcl_link(self):
        return 'https://cn.classic.warcraftlogs.com/reports/%s' % self.code


class Fight(models.Model):
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    fight_id = models.IntegerField(default=0)
    start = models.IntegerField(default=0, verbose_name="开始时间（timestamp毫秒）")
    end = models.IntegerField(default=0, verbose_name="结束时间（timestamp毫秒）")
    boss = models.IntegerField(default=0)
    kill = models.BooleanField(default=True, verbose_name="是否击杀")
    name = models.CharField(default="C'thun", max_length=50, verbose_name="名称")


class Friendly(models.Model):
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    name = models.CharField(default="xlinna", max_length=50, verbose_name="名称")
    friendly_id = models.IntegerField(default=0)
    guid = models.IntegerField(default=0)
    type = models.CharField(blank=True, null=True, max_length=50, verbose_name="职业")
    server = models.CharField(blank=True, null=True, max_length=50, verbose_name="服务器")

    def is_melee(self):
        if self.type in ('Warrior', 'Rogue'):
            return True
        else:
            return False


class Enemy(models.Model):
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    enemy_id = models.IntegerField(default=0)
    name = models.CharField(default="C'thun", max_length=50, verbose_name="名称")
    guid = models.IntegerField(default=0)
    type = models.CharField(blank=True, null=True, max_length=50, verbose_name="职业")


class LogDetail():
    def __init__(self, detail_type, detail_name, detail_scan_url, detail_info_url, scan_flag):
        self.detail_type = detail_type
        self.detail_name = detail_name
        self.detail_scan_url = detail_scan_url
        self.detail_info_url = detail_info_url
        self.scan_flag = scan_flag


class TemplateData():
    def __init__(self, fight_id, fight_name, kill, data):
        self.fight_id = fight_id
        self.fight_name = fight_name
        self.kill = kill
        self.data = data


class GoldRunTemplateData():
    def __init__(self, log, run_obj_list, warrior_all, paladin_all,
                 hunter_all, rogue_all, druid_all, mage_all, priest_all, warlock_all,
                 tank_fee, heal_fee, dps_fee, other_fee):
        self.log = log
        self.run_obj_list = run_obj_list
        self.warrior_all = warrior_all
        self.paladin_all = paladin_all
        self.hunter_all = hunter_all
        self.rogue_all = rogue_all
        self.druid_all = druid_all
        self.mage_all = mage_all
        self.priest_all = priest_all
        self.warlock_all = warlock_all
        self.tank_fee = tank_fee
        self.heal_fee = heal_fee
        self.dps_fee = dps_fee
        self.other_fee = other_fee
