from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Client, Mailing
from .serializers import ClientSerializer, MailingRetrieveSerializer, MailingSerializer


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = (IsAuthenticated,)


class MailingViewSet(ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
    # permission_classes = (IsAuthenticated,)

    action_to_serializer = {
        "retrieve": MailingRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(self.action, self.serializer_class)
