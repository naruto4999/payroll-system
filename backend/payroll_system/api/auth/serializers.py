from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from ..serializers import UserSerializer
from ..models import User
from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext as _
from django.contrib.auth.forms import SetPasswordForm

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Needs cleaning up
from django.contrib.auth import get_user_model
# User = get_user_model()
from api.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.html import strip_tags


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from builtins import str




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token



class LoginSerializer(MyTokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        # data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'phone_no']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print(user)
        return user

# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         PasswordResetForm({'email': value}).is_valid()
#         return value


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    frontend_url = serializers.URLField()

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username.")
        return user

    def validate(self, data):
        user = data['username']
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")

        return data

    def save(self):
        request = self.context.get('request')
        username = request.data.get('username')
        user = User.objects.get(username=username)
        email_template_name = 'api/password_reset_email.html'
        subject_template_name = 'registration/password_reset_subject.txt'
        frontend_url = self.validated_data.get('frontend_url')
        # generate the password reset token and email the user
        current_site = get_current_site(request)
        # site_name = current_site.name
        site_name = "PAY-PER"
        domain = current_site.domain
        domain = frontend_url
        c = {
            'frontend_url' : 'pass-confirm',
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = render_to_string(subject_template_name, c)
        email = render_to_string(email_template_name, c)
        email_text = strip_tags(email)

        send_mail(
            subject=subject.strip(),
            message=None,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=email,
            fail_silently=False,
        )





#serialiser for confirming password using django template
# class PasswordResetConfirmSerializer(serializers.Serializer):
#     new_password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     uid = serializers.CharField()
#     token = serializers.CharField()

#     def validate(self, attrs):
#         form = SetPasswordForm(user=self.context['user'], data=attrs)
#         if not form.is_valid():
#             raise serializers.ValidationError(form.errors)
#         return attrs

#     def create(self, validated_data):
#         self.context['user'].set_password(validated_data['new_password1'])
#         self.context['user'].save()
#         return self.context['user']


# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator

# User = get_user_model()

class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset request.
    """
    token = serializers.CharField()
    uid = serializers.CharField()
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        """
        Validate that the two password entries match and the token is valid.
        """
        # Decode the user id from the base64 encoded uidb64 string
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid reset link')

        # Check that the token is valid
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError('Invalid reset link')

        # Check that the two password entries match
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError({'detail': "The two password fields didn't match."})

        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        """
        Set the new password for the user.
        """
        password = self.validated_data['new_password1']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()



# class PasswordResetConfirmSerializer(serializers.Serializer):
#     """
#     Serializer for resetting user password.
#     """
#     token = serializers.CharField()
#     uidb64 = serializers.CharField()
#     new_password1 = serializers.CharField()
#     new_password2 = serializers.CharField()

#     def validate(self, attrs):
#         # Decode the uidb64 to uid
#         try:
#             uid = str(urlsafe_base64_decode(attrs['uidb64']))
#         except (TypeError, ValueError, OverflowError):
#             raise serializers.ValidationError('Invalid uidb64 value.')

#         # Get the user object
#         User = get_user_model()
#         try:
#             user = User.objects.get(pk=uid)
#         except User.DoesNotExist:
#             raise serializers.ValidationError('User does not exist.')

#         # Check that the token is valid for the user
#         if not default_token_generator.check_token(user, attrs['token']):
#             raise serializers.ValidationError('Invalid token.')

#         # Check that the new passwords match
#         if attrs['new_password1'] != attrs['new_password2']:
#             raise serializers.ValidationError('New passwords do not match.')

#         # Set the user object and the new password in validated data
#         attrs['user'] = user
#         attrs['new_password'] = attrs['new_password1']
#         return attrs

# class EmployeeRegisterSerializer(UserSerializer):
#     password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
#     email = serializers.EmailField(required=True, write_only=True, max_length=128)
#     owner = UserSerializer(read_only=True)


#     class Meta:
#         model = Employee
#         fields = ['id', 'username', 'email', 'password', 'is_active', 'owner']

#     def create(self, validated_data):
#         user = Employee.objects.create_user(**validated_data)
#         print(user)
#         return user



# class SubUserSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = SubUser
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


# class SubUserLoginSerializer(MyTokenObtainPairSerializer):
    
#     def validate(self, attrs):
#         data = super().validate(attrs)

#         refresh = self.get_token(self.user)

#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)

#         if api_settings.UPDATE_LAST_LOGIN:
#             update_last_login(None, self.user)

#         return data

# class SubUserRegisterSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
#     email = serializers.EmailField(required=True, write_only=True, max_length=128)

#     class Meta:
#         model = SubUser
#         fields = ['id', 'username', 'email', 'password', 'is_active', 'user']

#     def create(self, validated_data):
#         user = SubUser.objects.create_user(**validated_data)
#         return user
