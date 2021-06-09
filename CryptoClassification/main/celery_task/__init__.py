# -*- coding: utf-8 -*-

from celery import Celery

celery_app = Celery("celeryTasks")
celery_app.config_from_object("main.celery_task.CeleryConfig")