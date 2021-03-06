from django.urls import re_path, path
from file_upload import views
from base.views import load_report, log_detail, log_list, scan_viscidus_poison_tick, viscidus_poison_tick_info,\
    scan_boss_nature_protection, boss_nature_protection_info, gold_run_detail

# namespace
app_name = "base"

urlpatterns = [

    # Upload File Without Using Model Form
    re_path(r'^upload1/$', views.file_upload, name='file_upload'),

    # Upload Files Using Model Form
    re_path(r'^upload2/$', views.model_form_upload, name='model_form_upload'),

    # Upload Files Using Ajax Form
    re_path(r'^upload3/$', views.ajax_form_upload, name='ajax_form_upload'),

    # Handling Ajax requests
    re_path(r'^ajax_upload/$', views.ajax_upload, name='ajax_upload'),

    re_path(r'^parse/(?P<pk>\d+)', views.parse, name='parse'),

    re_path(r'^poison/(?P<pk>\d+)/', views.poison_data, name='poison'),

    # View Log List
    path('', view=log_list, name='log_list'),

    # load report
    re_path(r'^loadreport/$', view=load_report, name='load_report'),

    # re_path(r'submitreport/(?P<code>\d+)$', load_report, name='submit'),

    # log detail
    re_path(r'^log_detail/(?P<id>\d+)', view=log_detail, name='log_detail'),

    # gold run detail
    re_path(r'^gold_run_detail/(?P<id>\d+)', view=gold_run_detail, name='gold_run_detail'),

    # scan task
    re_path(r'^scan_viscidus_poison_tick/(?P<log_id>\d+)$', view=scan_viscidus_poison_tick, name='scan_viscidus_poison_tick'),

    re_path(r'^viscidus_poison_tick_info/(?P<log_id>\d+)$', view=viscidus_poison_tick_info, name='viscidus_poison_tick_info'),

    re_path(r'^scan_boss_nature_protection/(?P<log_id>\d+)$', view=scan_boss_nature_protection, name='scan_boss_nature_protection'),

    re_path(r'^boss_nature_protection_info/(?P<log_id>\d+)$', view=boss_nature_protection_info, name='boss_nature_protection_info'),
]