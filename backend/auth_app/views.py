import os

from django.http import HttpResponseRedirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .services import response_with_tokens_in_cookies


class CheckAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"isAuthenticated": True})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]

            response = response_with_tokens_in_cookies(response, access_token, refresh_token)
        return response


class GoogleCompleteView(APIView):
    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')

        response = HttpResponseRedirect(os.environ.get("OAUTH_REDIRECT_URL"))
        if access_token and refresh_token:
            response = response_with_tokens_in_cookies(response, access_token, refresh_token)
        return response
