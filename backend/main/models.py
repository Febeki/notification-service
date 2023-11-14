from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager
from .tasks import send_message_to_client
from .utils import time_to_send_message


class User(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"


class Client(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    mobile_operator_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.phone_number} {self.mobile_operator_code} {self.tag}"


class Mailing(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    message_text = models.TextField()
    client_filter = models.CharField(max_length=150, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.client_filter:
            tag, mobile_operator_code = self.client_filter.split()
            clients = Client.objects.filter(tag=tag, mobile_operator_code=mobile_operator_code)
        else:
            clients = Client.objects.all()
        for cl in clients:
            start_function_at = time_to_send_message(cl.timezone, self.start_time, self.end_time)
            if start_function_at:
                send_message_to_client.apply_async(args=[cl.id, self.id], eta=start_function_at)

    def __str__(self):
        return f"Mailing {self.id}"


class Message(models.Model):
    DELIVERED = "D"
    DELIVERY_ERROR = "E"
    DELIVERY_IN_PROCESS = "P"

    STATUSES = [
        (DELIVERED, "Доставлено"),
        (DELIVERY_ERROR, "Ошибка"),
        (DELIVERY_IN_PROCESS, "Отправляется"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUSES)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id}"
