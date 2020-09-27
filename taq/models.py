from django.db import models
from base.models import Fight, WCLLog, Friendly, Enemy

# Create your models here.

# 维希度斯毒箭dot数据
class ViscidusPoisonTick(models.Model):
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE)
    friendly = models.ForeignKey(Friendly, on_delete=models.CASCADE)
    name = models.CharField(default="一夜鱼龙舞", max_length=100)
    damage = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    tick = models.IntegerField(default=0)
    uptime = models.FloatField(default=0.0)


# 克苏恩小眼伤害
class EyeTentacleDamage(models.Model):
    pass


# 公主维希度斯奥罗克苏恩 自然吸收统计
class BossNatureProtection(models.Model):
    IMPORTANCE_L1 = 'L1'
    IMPORTANCE_L2 = 'L2'
    IMPORTANCE_L3 = 'L3'
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE)
    friendly = models.ForeignKey(Friendly, on_delete=models.CASCADE)
    name = models.CharField(default="一夜鱼龙舞", max_length=100)
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)
    nature_protection_absorb = models.IntegerField()
    nature_protection_cast = models.IntegerField()
    nature_protection_uptime = models.FloatField()
    major_nature_protection_absorb = models.IntegerField()
    major_nature_protection_cast = models.IntegerField()
    major_nature_protection_uptime = models.FloatField()
    importance = models.CharField(max_length=20, default='L3')


# C帝金团分金明细
class TaqGoldRunDetail(models.Model):
    log = models.ForeignKey(WCLLog, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    classic = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    titan = models.IntegerField(default=0)
    tank = models.IntegerField(default=0)
    heal_total = models.IntegerField(default=0)
    heal_classic = models.IntegerField(default=0)
    heal_boss = models.IntegerField(default=0)
    dispel = models.IntegerField(default=0)
    dps_total_melee = models.IntegerField(default=0)
    dps_total_range = models.IntegerField(default=0)
    dps_punishment = models.IntegerField(default=0)
    dps_boss = models.IntegerField(default=0)
    dps_qiraji_champion = models.IntegerField(default=0)
    dps_qiraji_slayer = models.IntegerField(default=0)
    dps_qiraji_mindslayer = models.IntegerField(default=0)
    dps_obsidian_nullifier = models.IntegerField(default=0)
    jumper = models.IntegerField(default=0)
    other_punishment = models.IntegerField(default=0)
    base_gold = models.IntegerField(default=0)
    total_gold = models.IntegerField(default=0)

    def reset(self):
        self.tag = ''
        self.titan = 0
        self.tank = 0
        self.heal_total = 0
        self.heal_classic = 0
        self.heal_boss = 0
        self.dispel = 0
        self.dps_total_melee = 0
        self.dps_total_range = 0
        self.dps_punishment = 0
        self.dps_boss = 0
        self.dps_qiraji_champion = 0
        self.dps_qiraji_slayer = 0
        self.dps_qiraji_mindslayer = 0
        self.dps_obsidian_nullifier = 0
        self.jumper = 0
        self.other_punishment = 0
        self.base_gold = 0
        self.total_gold = 0
        self.save()

    def all_fee(self):
        return self.titan \
               + self.tank \
               + self.heal_total \
               + self.heal_classic \
               + self.heal_boss \
               + self.dispel \
               + self.dps_total_melee \
               + self.dps_total_range \
               + self.dps_punishment \
               + self.dps_boss \
               + self.dps_qiraji_champion \
               + self.dps_qiraji_slayer \
               + self.dps_qiraji_mindslayer \
               + self.dps_obsidian_nullifier \
               + self.jumper \
               + self.other_punishment

    def color_code(self):
        if self.classic == 'Warrior':
            return '#B8860B'
        elif self.classic == 'Paladin':
            return '#FF69B4'
        elif self.classic == 'Hunter':
            return '#9ACD32'
        elif self.classic == 'Rogue':
            return '#FFD700'
        elif self.classic == 'Druid':
            return '#FF8C00'
        elif self.classic == 'Mage':
            return '#00BFFF'
        elif self.classic == 'Priest':
            return '#FFFFFF'
        elif self.classic == 'Warlock':
            return '#7B68EE'
        else:
            return '#FF0000'
