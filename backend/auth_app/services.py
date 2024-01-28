from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


def validated_response(request: HttpRequest, get_response: Callable, access_token: str, refresh_token: str):
    try:
        AccessToken(access_token)
    except TokenError:
        response = get_response(request)
        try:
            valid_token = RefreshToken(refresh_token)
            return response_with_tokens_in_cookies(response, str(valid_token.access_token), str(refresh_token))
        except TokenError:
            return response_without_tokens(response)
    request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    return None


def response_with_tokens_in_cookies(response: HttpResponse, access_token: str, refresh_token: str) -> HttpResponse:
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=settings.USE_HTTPS
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=settings.USE_HTTPS
    )
    return response


def response_without_tokens(response: HttpResponse) -> HttpResponse:
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
