# _*_coding : uft-8 _*_
# @Time : 2023/6/15 13:10
# @Author : 
# @File : main
# @Project : meiduo_drf
from celery import Celery
import os

# celery -A celery_tasks.main worker --concurrency=4 --loglevel=INFO -P threads     # 运行celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hzmeilan.settings')  # 为celery的运行设置django的环境

celery_app = Celery('meiduo')  # 创建celery实例对象
celery_app.config_from_object('celery_tasks.config')  # 加载配置文件
celery_app.autodiscover_tasks(['celery_tasks.sms'])  # 自动注册异步任务
