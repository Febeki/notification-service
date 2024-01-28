from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register("clients", views.ClientViewSet, basename="clients")
router.register("mailing", views.MailingViewSet, basename="mailing")

urlpatterns = [

]

urlpatterns += router.urls
