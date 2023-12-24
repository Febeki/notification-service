from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField

from .managers import UserManager


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
    task_ids = ArrayField(models.CharField(max_length=36), default=list)

    def __str__(self):
        return f"Mailing {self.pk}"


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
        return f"Message {self.pk}"
