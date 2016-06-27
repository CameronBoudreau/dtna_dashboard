from django.apps import AppConfig
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import filelock


class DataProcessorConfig(AppConfig):
    name = 'data_processor'
