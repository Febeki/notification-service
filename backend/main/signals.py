from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from main.services.model_services import (
    create_celery_tasks_to_send_messages_to_clients, get_clients_by_filter,
    revoke_celery_tasks_by_ids)

from .models import Mailing


@receiver(pre_save, sender=Mailing)
def pre_save_mailing(sender, instance, update_fields, **kwargs):
    if instance.pk and update_fields != frozenset({'task_ids'}):
        revoke_celery_tasks_by_ids(instance.task_ids)


@receiver(post_save, sender=Mailing)
def post_save_mailing(sender, instance, update_fields, **kwargs):
    if update_fields != frozenset({'task_ids'}):
        task_ids = create_celery_tasks_to_send_messages_to_clients(
            clients=get_clients_by_filter(instance.client_filter),
            instance=instance
        )
        instance.task_ids = task_ids
        instance.save(update_fields=['task_ids'])


@receiver(pre_delete, sender=Mailing)
def pre_delete_mailing(sender, instance, **kwargs):
    revoke_celery_tasks_by_ids(instance.task_ids)
