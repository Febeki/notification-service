from django.core.validators import RegexValidator
from django.db.utils import IntegrityError
from rest_framework import serializers

from .models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=11,
        validators=[RegexValidator(r'^7\d{10}$', message="Номер телефона должен быть в формате 7XXXXXXXXXXX")]
    )
    mobile_operator_code = serializers.CharField(
        max_length=3,
        validators=[RegexValidator(r'^\d{3}$', message="Код оператора должен состоять из трех цифр")]
    )
    tag = serializers.CharField(
        max_length=100,
        validators=[RegexValidator(r'^[a-zA-Z]+\d*$',
                                   message="Тег должен состоять из букв или букв и цифр в конце, \
                                   без пробелов и специальных символов")]
    )

    def handle_integrity_error(self, exc):
        raise serializers.ValidationError({
            "phone_number": [
                "Клиент с таким номером телефона уже существует!"
            ]
        })

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            self.handle_integrity_error(exc)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as exc:
            self.handle_integrity_error(exc)

    class Meta:
        model = Client
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    client = ClientSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    client_filter = serializers.CharField(
        max_length=150,
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[RegexValidator(r'^\S+\s\d{3}$',
                                   message="фильтр должен быть в формате: '{Тег} {Код оператора}' ")]
    )

    class Meta:
        model = Mailing
        exclude = ('task_ids',)


class MailingRetrieveSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Mailing
        exclude = ('task_ids',)

    def get_messages(self, obj):
        messages = obj.message_set.all().select_related('client').order_by("status")
        return MessageSerializer(messages, many=True).data
