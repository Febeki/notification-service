import os

import requests

from main.models import Client, Mailing, Message


def _send_message_to_external_api(msg: dict) -> int:
    """send message to external api and return response status code"""
    response = requests.post(f'https://probe.fbrq.cloud/v1/send/{msg["id"]}',
                             json=msg,
                             headers={'Authorization': f'Bearer {os.environ.get("JWT_TOKEN")}'},
                             timeout=30)
    return response.status_code


def create_message(client_id: int, mailing_id: int) -> Message:
    """create message in database and return message instance"""
    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)

    message = Message.objects.create(client=client, mailing=mailing, status=Message.DELIVERY_IN_PROCESS)

    return message


def send_message_and_set_status(message: Message) -> None:
    """send message and set response status code"""
    dict_message = {
        "id": message.pk,
        "phone": int(message.client.phone_number),
        "text": message.mailing.message_text,
    }
    try:
        satus_code = _send_message_to_external_api(dict_message)
        if satus_code == 200:
            message.status = Message.DELIVERED
        else:
            message.status = Message.DELIVERY_ERROR
    except requests.RequestException:
        message.status = Message.DELIVERY_ERROR

    message.save()
