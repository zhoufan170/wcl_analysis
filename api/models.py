from django.db import models
import uuid


# Create your models here.
class ApiToken(models.Model):
    """
    Api token,用于api调用方授权
    """
    name = models.CharField('描述', max_length=100)
    token = models.CharField('签名令牌', max_length=50, help_text='后端自动生成', default=str(uuid.uuid1()))
    creator = models.CharField('创建人', max_length=50)
    gmt_created = models.DateTimeField('创建时间', auto_now_add=True)
    gmt_modified = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        verbose_name = '调用token'
        verbose_name_plural = '调用token'