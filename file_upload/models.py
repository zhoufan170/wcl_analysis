# -*- coding:utf-8 -*-
from django.db import models
import os
import uuid
import datetime

# Create your models here.
# Define user directory path


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", filename)


class File(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=True)
    absolute_file = models.CharField(max_length=100, verbose_name="原文件名", default='poison.txt')
    wcl_link = models.CharField(max_length=200, verbose_name="wcl链接", default="https://cn.classic.warcraftlogs.com/")
    parse_flag = models.BooleanField(default=False)
    upload_time = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.absolute_file

    def format_upload_time(self):
        return (self.upload_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


class PoisonData(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, verbose_name="username", default='一夜鱼龙舞')
    amount = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    tick = models.IntegerField(default=0)
    uptime = models.FloatField(default=0.0)

    def __unicode__(self):
        return '%d:%s' % (self.file.absolute_file, self.username)