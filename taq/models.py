from django.db import models
from base.models import Fight, WCLLog, Friendly

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