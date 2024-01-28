from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import User


def custom_auth_rule(user):
    # india_timezone = 'Asia/Kolkata'
    # timezone.activate(india_timezone)
    # current_time_in_india = timezone.now()
    # timezone.deactivate()
    print("CUSTOM AUTH RULE")
    if user:
        if user.is_subscription_active():
            return True
        else:
            # raise serializers.ValidationError("Subscription has ended. Please renew your subscription to log in.")
            raise AuthenticationFailed(detail="Subscription has ended. Please renew your subscription to log in.")
    else:
        return False

class CustomRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs['refresh']
        print(f"RUNNING CUSTOM SERIALIZER")

        # Extract user ID from refresh token payload
        try:
            user_id = RefreshToken(refresh).get('user_id')
            print(f'User ID: {user_id}')
        except TokenError:
            raise AuthenticationFailed(detail='Invalid refresh token')

        # # Retrieve the user based on user ID
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed(detail='User not found')

        # Check subscription status
        if not user.is_subscription_active():
            raise AuthenticationFailed(detail='Subscription has ended. Cannot refresh token.')

        return super().validate(attrs)

# class TokenRefreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField()
#     access = serializers.CharField(read_only=True)
#     token_class = RefreshToken

#     def validate(self, attrs):
#         print(f"RUNNING CUSTOM REFRESH VIEWWWW")
#         refresh = self.token_class(attrs["refresh"])

#         data = {"access": str(refresh.access_token)}

#         if api_settings.ROTATE_REFRESH_TOKENS:
#             if api_settings.BLACKLIST_AFTER_ROTATION:
#                 try:
#                     # Attempt to blacklist the given refresh token
#                     refresh.blacklist()
#                 except AttributeError:
#                     # If blacklist app not installed, `blacklist` method will
#                     # not be present
#                     pass

#             refresh.set_jti()
#             refresh.set_exp()
#             refresh.set_iat()

#             data["refresh"] = str(refresh)

#         return data
