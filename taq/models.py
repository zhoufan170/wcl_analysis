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
