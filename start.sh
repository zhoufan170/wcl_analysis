#!/bin/sh

# 启动celery
nohup celery -A wcl_analysis worker -l info -Q wcl_analysis > /tmp/wcl_celery.log
# 启动web
nohup python3 manage.py runserver 0.0.0.0:8080 > /tmp/wcl_web.log