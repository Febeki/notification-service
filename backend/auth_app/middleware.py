# middleware.py
from django.utils.deprecation import MiddlewareMixin


class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_token = request.COOKIES.get('access_token')
        print(request.COOKIES)
