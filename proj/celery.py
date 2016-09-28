import os

from celery import Celery


CELERY_MAIN = 'tasks'
BROKER_DETAILS = dict(user=os.environ.get('CELERY_BROKER_USERNAME'),
                          password=os.environ.get('CELERY_BROKER_PASSWORD'),
                          server=os.environ.get('CELERY_BROKER_SERVER'),
                          port=os.environ.get('CELERY_BROKER_PORT'),
                          vhost=os.environ.get('CELERY_BROKER_VHOST'))
CELERY_BROKER_URL = 'amqp://{user}:{password}@{server}:{port}/{vhost}'.format(**BROKER_DETAILS)

CELERY_CONFIG = dict(
    CELERY_RESULT_BACKEND = 'amqp://{user}:{password}@{server}:{port}/{vhost}'.format(**BROKER_DETAILS),
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TRACK_STARTED = True,
    CELERY_TIMEZONE = 'US/Pacific'
    )

celery = Celery(CELERY_MAIN, 
                broker=CELERY_BROKER_URL, 
                include=['proj.tasks.ascii'])
celery.conf.update(CELERY_CONFIG)

if __name__ == '__main__':
  celery.start()
