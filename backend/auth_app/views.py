from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework.views import APIView


class GoogleCompleteView(APIView):
    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')

        if access_token and refresh_token:
            # Перенаправляем на фронтенд с токенами в URL
            frontend_url = f"http://localhost:3000/google-auth-callback?access_token={access_token}&refresh_token={refresh_token}"
            return redirect(frontend_url)
        else:
            # Если токены не найдены, отправляем сообщение об ошибке
            return JsonResponse({'error': 'Authentication failed'}, status=401)

