from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def associate_by_email(**kwargs):

    try:
        email = kwargs['details']['email']

        kwargs['user'] = User.objects.get(email=email)
        refresh = RefreshToken.for_user(kwargs['user'])
        kwargs['strategy'].session_set('access_token', str(refresh.access_token))
        kwargs['strategy'].session_set('refresh_token', str(refresh))

    except User.DoesNotExist:
        pass
    return kwargs
