from typing import Optional

from celery.result import AsyncResult
from django.db.models import QuerySet

from main.models import Client, Mailing
from main.tasks import send_message_to_client
from main.utils import time_to_send_message


def create_celery_tasks_to_send_messages_to_clients(clients: QuerySet[Client], instance: Mailing) -> list:
    """Create celery tasks and return task ids"""
    task_ids = []

    clients_with_message = instance.message_set.values_list('client_id', flat=True)

    for cl in clients:
        if cl.pk in clients_with_message:
            continue

        start_function_at = time_to_send_message(cl.timezone, instance.start_time, instance.end_time)
        if start_function_at:
            task = send_message_to_client.apply_async(args=[cl.pk, instance.pk], eta=start_function_at)
            task_ids.append(task.id)

    return task_ids


def get_clients_by_filter(client_filter: Optional[str]) -> QuerySet[Client]:
    """Return filtered clients by client_filter.
    If client_filter is None, return all clients"""
    if client_filter:
        tag, mobile_operator_code = client_filter.split()
        clients = Client.objects.filter(tag=tag, mobile_operator_code=mobile_operator_code)
    else:
        clients = Client.objects.all()
    return clients


def revoke_celery_tasks_by_ids(task_ids: list[str]) -> None:
    """Revoke celery tasks by task_ids"""

    for task_id in task_ids:
        AsyncResult(task_id).revoke(terminate=True)
