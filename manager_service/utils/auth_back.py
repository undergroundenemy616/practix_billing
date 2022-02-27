from django.utils.translation import gettext_lazy as _
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (AuthenticationFailed,
                                                 InvalidToken, TokenError)
from subscribtions.models import Account


class SubscriptionJWTAuth(JWTAuthentication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = Account

    def get_user(self, validated_token):
        from auth_grpc.set_role import check_user_exits
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))
        user = self.user_model.objects.filter(**{api_settings.USER_ID_FIELD: user_id}).first()
        if not user:
            if not check_user_exits(user_id):
                raise AuthenticationFailed(_('User not found'), code='user_not_found')
            user = Account.objects.create(id=user_id)
        return user
