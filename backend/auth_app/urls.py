from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('api/check/login/', views.CheckAuth.as_view(), name='check-auth'),
    path("api/token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/complete/google-oauth2/', views.GoogleCompleteView.as_view(), name="google_complete"),
]
