from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken


class CustomRefreshToken(RefreshToken):

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['is_staff'] = user.is_staff
        return token


User = get_user_model()


def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
        tokens = CustomRefreshToken.for_user(kwargs['user'])
        kwargs['request'].session['access_token'] = str(tokens.access_token)
        kwargs['request'].session['refresh_token'] = str(tokens)
    except User.DoesNotExist:
        pass
    return kwargs
