from celery import shared_task

from main.services.task_services import create_message, send_message_and_set_status


@shared_task
def send_message_to_client(client_id, mailing_id):
    print("START TO SEND MESSAGES")
    message = create_message(client_id, mailing_id)
    send_message_and_set_status(message)
    print("END TO SEND MESSAGES")
