import djcelery

djcelery.setup_loader()


CELERY_QUEUES = {
    'beat_tasks':{
        'exchange':'beat_tasks',
        'exchange_type':'direct',
        'binding_key':'beat_tasks',
    },
    'worker_queue': {
        'exchange': 'worker_queue',
        'exchange_type': 'direct',
        'binding_key': 'worker_queue',
    },

}

CELERY_DEFAULT_QUEUE = 'worker_queue'

CELERY_IMPORTS = (
    'apps.video.tasks'
)

#某些情况防止死锁
CELERYD_FORCE_EXECV = True


#设置并发的worker数
CELERYD_CONCURRENCY = 4


#允许重试
CELERY_ACKS_LATE = True


#每个worker最多执行100个任务,防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 100


#单个任务的最大运行时间
CELERY_TASK_TIME_LIMIT = 12 * 30