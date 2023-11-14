import os

import requests
from celery import shared_task
from requests.exceptions import RequestException


@shared_task
def send_message_to_client(client_id, mailing_id):
    from .models import Client, Mailing, Message

    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)

    message = Message.objects.create(client=client, mailing=mailing, status=Message.DELIVERY_IN_PROCESS)

    msg = {
        "id": message.id,
        "phone": int(client.phone_number),
        "text": mailing.message_text,
    }

    try:
        response = requests.post(f'https://probe.fbrq.cloud/v1/send/{msg["id"]}',
                                 json=msg,
                                 headers={'Authorization': f'Bearer {os.environ.get("JWT_TOKEN")}'},
                                 timeout=30)
        if response.status_code == 200:
            message.status = Message.DELIVERED
        else:
            message.status = Message.DELIVERY_ERROR
    except RequestException:
        message.status = Message.DELIVERY_ERROR

    message.save()
