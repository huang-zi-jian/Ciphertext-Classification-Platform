# -*- coding: utf-8 -*-
from celery.schedules import crontab
from kombu import Exchange, Queue

BROKER_URL = "redis://:feifei@122.51.255.207:6379/0"
CELERY_RESULT_BACKEND = "redis://:feifei@122.51.255.207:6379/1"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# 任务执行结果的超时时间
CELERY_TSKK_RESULT_EXPIRES = 60 * 60 * 24 * 3
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "Asia/Shanghai"

# 并发的worker数量
CELERY_CONCURRENCY = 10

# 每个worker执行多少次任务后会死掉
# CELERY_MAX_TASK_PER_CHILD = 100

# 单个任务运行的时间限制，超时会被杀死
# CELERY_TASK_SOFT_TIME_LIMIT = 300

# 关闭执行限速
CELERY_DISABLE_RATE_LIMITS = True

CELERY_IMPORTS = (
    "main.celery_task.celeryTasks",
)

# 优先级队列设置
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_QUEUES = (
    # celery是设置的队列名
    # Exchange 是交换机的名称
    # routing_key 交换机跟队列交流的key

    # Queue('task_slow', exchange=Exchange('task_slow'), routing_key='task_slow'),
    Queue("features_celery", Exchange("features_celery"), routing_key="features_celery",
          queue_arguments={'x-max-priority': 3}),
    Queue("capture_celery", Exchange("capture_celery"), routing_key="capture_celery",
          queue_arguments={'x-max-priority': 3})
)

# 将任务分配到不同的队列
CELERY_ROUTES = {
    'main.celery_task.celeryTasks.features_Generate': {'queue': 'features_celery', 'routing_key': 'features_celery'},
    'main.celery_task.celeryTasks.netpackage_capture': {'queue': 'capture_celery', 'routing_key': 'capture_celery'}
}


# CELERYBEAT_SCHEDULE = {
#     'cipher_task': {
#         'task': 'main.celery_task.celeryTasks.cipher_task',
#         'schedule': crontab(minute='*/1'),
#         'args': (),
#     },
#     'modelTrain_task': {
#         'task': 'main.celery_task.celeryTasks.modelTrain_task',
#         'schedule': crontab(minute='*/1'),
#         'args': (),
#     }
# }