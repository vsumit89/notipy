from celery import Celery, Task
from celery.utils.log import get_task_logger
import asyncio

from utils.config import get_settings
from utils.file import process_urls

from app.models.channels import ChannelType, EmailChannel
from app.models.notifications import NotificationStatus

from app.external.notifications.notification_factory import get_notification_service
from app.external.notifications.email import EmailData

from app.repositories.db_factory import getDB
from app.repositories.notification.notifications_factory import (
    get_notifications_repository,
)

settings = get_settings()

logger = get_task_logger(__name__)


celery_app = Celery(
    "notification worker",
    broker=f"amqp://{settings.MQ_USERNAME}:{settings.MQ_PASSWORD}@{settings.MQ_HOST}:{settings.MQ_PORT}/{settings.MQ_VHOST}",
)


async def update_notification_status(notification_id: str, status: str):
    try:
        settings = get_settings()
        db = getDB(settings.DB_STORE)
        await db.connect()

        repository = get_notifications_repository(settings.DB_STORE)
        await repository.update_notification_status(
            id=notification_id,
            status=status,
        )
    except:
        raise Exception("error in updating notification status", str(e))


class NotificationTask(Task):
    def run(
        self,
        notification_id: str,
        channel_type: str,
        channel_data: dict,
        dynamic_data: dict,
    ):
        try:
            print("this is data", dynamic_data)
            channel_data = EmailChannel(
                **channel_data,
            )
            notification_service = get_notification_service(channel_type)

            notification_data = None
            match channel_type:
                case ChannelType.EMAIL.value:
                    content = notification_service.render_template(
                        channel_data.content,
                        dynamic_data["metadata"],
                        channel_data.is_html,
                    )

                    files = asyncio.run(process_urls(dynamic_data["attachments"]))

                    notification_data = EmailData(
                        to_email=dynamic_data["to_email"],
                        subject=channel_data.subject,
                        content=content,
                        is_html=channel_data.is_html,
                        attachments=files,
                    )

                case ChannelType.SMS.value:
                    raise NotImplementedError(
                        f"channel type {channel_type} is not implemented"
                    )
                case _:
                    raise NotImplementedError(
                        f"channel type {channel_type} is not implemented"
                    )

            max_retries = 3
            while max_retries > 0:
                is_sent = notification_service.send_notification(notification_data)
                if is_sent:
                    break
                max_retries -= 1

            if max_retries == 0:
                asyncio.run(
                    update_notification_status(
                        notification_id=notification_id,
                        status=NotificationStatus.FAILED,
                    )
                )
            else:
                asyncio.run(
                    update_notification_status(
                        notification_id=notification_id,
                        status=NotificationStatus.SUCCESS,
                    )
                )

        except Exception as e:
            raise e


@celery_app.task(name="send_notification")
def send_notifications(
    notification_id: str,
    channel_type: str,
    channel_data: dict,
    dynamic_data: dict,
):
    print("in the task", dynamic_data)
    NotificationTask().run(
        notification_id=notification_id,
        channel_type=channel_type,
        channel_data=channel_data,
        dynamic_data=dynamic_data,
    )


celery_app.register_task(send_notifications)
