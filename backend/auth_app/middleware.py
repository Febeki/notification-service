from django.utils.deprecation import MiddlewareMixin

from .services import validated_response


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token or not refresh_token:
            return None

        return validated_response(request, self.get_response, access_token, refresh_token)
