
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Worker

logger = logging.getLogger('core')


@receiver(post_save, sender=Worker)
def log_worker_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(
            f'{instance.created_by} создал сотрудника '
            f'{instance.get_full_name()} id {instance.id}'
        )
