from celery import Celery, Task
from utils.config import get_settings
from celery.utils.log import get_task_logger
import time

settings = get_settings()

logger = get_task_logger(__name__)


celery_app = Celery(
    "notification worker",
    broker=f"amqp://{settings.MQ_USERNAME}:{settings.MQ_PASSWORD}@{settings.MQ_HOST}:{settings.MQ_PORT}/{settings.MQ_VHOST}",
)


class NotificationTask(Task):
    max_retries = 3
    default_retry_delay = 10

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.info("Retrying task: --->>>> ")
        return

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("Task failed: --->>>> ")
        return

    def run(self, param):
        try:
            for i in range(10):
                print("sending notifications ---->", i)

            time.sleep(3)
            raise Exception("Exception occured")

        except Exception as e:
            self.retry(exc=e)


@celery_app.task(name="send_notification")
def send_notifications():
    NotificationTask().run("sumit")


celery_app.register_task(send_notifications)
