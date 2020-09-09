from celery import Celery
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wcl_analysis.settings')
import django
django.setup()

app = Celery('wcl_analysis', broker='redis://127.0.0.1:6379/1')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
from service.taq_service import TaqService
from service.base_service import BaseService
from service.constant import CONSTANT_SERVICE


@app.task
def test_task():
    print("begin to run task")
    import time
    time.sleep(30)
    print("end to run task")

@app.task
def viscidus_poison_tick_task(log_id):
    # BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK, flag=-1)
    print("begin to run viscidus_poison_tick_task")
    result, msg = TaqService.viscidus_poison_tick(log_id=log_id)
    if result:
        print("viscidus_poison_tick_task run success")
        BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK, flag=1)
    else:
        print("viscidus_poison_tick_task run fail")
        BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.VISCIDUS_POISON_TICK_TASK, flag=0)

@app.task
def boss_nature_protection_task(log_id):
    result, msg = TaqService.nature_protection_summary(log_id=log_id)
    if result:
        BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.BOSS_NATURE_PROTECTION, flag=1)
    else:
        BaseService.update_sync_flag(log_id=log_id, task=CONSTANT_SERVICE.BOSS_NATURE_PROTECTION, flag=0)