CELERY_IGNORE_RESULT = False
BROKER_URL = "amqp://admin:mypass@127.0.0.1:5673"
CELERY_RESULT_BACKEND = "amqp"
CELERY_ROUTES = {
    "atr.worker.Executor": {'queue': 'tasks'}
}
