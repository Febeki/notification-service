from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("clients", views.ClientViewSet, basename="clients")
router.register("mailing", views.MailingViewSet, basename="mailing")

urlpatterns = [
    path('mailing-detail/<int:pk>/', views.DetailMailingView.as_view(), name='detailed-mailing'),
]

urlpatterns += router.urls
