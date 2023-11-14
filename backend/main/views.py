from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Client, Mailing
from .serializers import ClientSerializer, DetailMailingSerializer, MailingSerializer, MessageSerializer


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (IsAuthenticated,)


class MailingViewSet(ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    permission_classes = (IsAuthenticated,)


class DetailMailingView(RetrieveAPIView):
    queryset = Mailing.objects.all()
    serializer_class = DetailMailingSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        messages = instance.message_set.all().select_related('client').order_by("status")
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['messages'] = MessageSerializer(messages, many=True).data
        return Response(data)
