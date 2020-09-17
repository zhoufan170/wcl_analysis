#!/bin/sh

# 启动celery
sudo systemctl restart wclcelery
# 启动web
sudo systemctl restart wclweb
# 启动jupyter notebook(运行脚本用)
sudo systemctl restart jupyter
