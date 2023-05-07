from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import generics, views
from .serializers import LoginSerializer, RegisterSerializer, MyTokenObtainPairSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, OTPSerializer
from django.utils.translation import gettext as _
from django.contrib.auth.views import (
    PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from api.models import OTP
from django.core.mail import send_mail
import random
from datetime import timedelta
from django.conf import settings
from django.utils import timezone


# extra
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from .serializers import PasswordResetConfirmSerializer
from django.contrib.auth.forms import SetPasswordForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# from ..models import User


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class VerifyOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        otp_obj = OTP.objects.filter(email=email).last()

        if not otp_obj:
            return Response({
                'detail': 'Invalid OTP.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not otp_obj.is_valid() or otp_obj.otp != otp:
            return Response({
                'detail': 'Invalid OTP.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user account
        # 'id', 'username', 'email', 'password', 'is_active', 'phone_no'
        user_data = serializer.validated_data
        del user_data['otp']
        print(f'user data: {user_data}')

        user = User.objects.create_user(**user_data)
        # refresh = RefreshToken.for_user(user)
        # access_token = str(refresh.access_token)

        return Response({
            'detail': "Account Successfuly Created"
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView, MyTokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView, MyTokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # refresh = RefreshToken.for_user(user)
        # res = {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token),
        # }
         # Generate and send OTP
        email = serializer.validated_data['email']
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=5)
        OTP.objects.create(email=email, otp=otp, expires_at=expires_at)
        send_mail(
            'Your OTP for registration',
            f'Your OTP is {otp}. This OTP will expire in 5 minutes.',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response({
            'detail': 'An OTP has been sent to your email address.'
        }, status=status.HTTP_200_OK)
        # return Response({
            # "detail": "Account created successfully",
            # "user": serializer.data,
            # "refresh": res["refresh"],
            # "token": res["access"]
        # }, status=status.HTTP_201_CREATED)


class RefreshView(generics.CreateAPIView, TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class PasswordResetView(BasePasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'


# class PasswordResetAPIView(generics.GenericAPIView):
#     serializer_class = PasswordResetSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data['email']
#         PasswordResetView.as_view()(request=request, from_email='myanimecollection06@gmail.com', email_template_name='registration/password_reset_email.html')

#         return Response({'detail': _('Password reset email has been sent.')}, status=status.HTTP_200_OK)


class PasswordResetAPIView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response({'detail': _('Password reset email has been sent.')}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    template_name = 'api/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        self.user = self.get_user(uidb64)
        # print(self.user)
        # print(default_token_generator.check_token(self.user, token))
        if not self.user or not default_token_generator.check_token(self.user, token):
            return Response({'detail': _('Invalid reset link.')}, status=status.HTTP_400_BAD_REQUEST)

        context = {
            'form': SetPasswordForm(user=self.user),
            'validlink': True,
        }
        return Response(context, template_name=self.template_name)

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        self.user = self.get_user(uidb64)
        print("yay")
        print(self.user)
        print(request.data)
        print(default_token_generator.check_token(self.user, token))
        if not self.user or not default_token_generator.check_token(self.user, token):
            return Response({'detail': _('Invalid reset link.')}, status=status.HTTP_400_BAD_REQUEST)
        
        data = dict(request.data)
        token_recieved = data.pop('csrfmiddlewaretoken')
        print(type(token_recieved))
        data['token'] = token
        data['uid'] = uidb64
        data['new_password1'] = request.POST['new_password1']
        data['new_password2'] = request.POST['new_password2']
        print(data)
        serializer = self.get_serializer(data=data, context={'user': self.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        context = {
            'form': SetPasswordForm(user=self.user),
            'validlink': True,
            'success_url': self.success_url,
        }
        # return Response(context, template_name=self.template_name)
        return redirect(self.success_url)

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None



class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get('uidb64', None)
        token = request.data.get('token', None)
        new_password1 = request.data.get('new_password1', None)
        new_password2 = request.data.get('new_password2', None)
        print(new_password1)
        print(new_password2)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'uid': uidb64,
            'token': token,
            'new_password1': new_password1,
            'new_password2': new_password2,
        }

        serializer = self.serializer_class(data=data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password has been reset successfully'}, status=status.HTTP_200_OK)



# class PasswordResetConfirmView(generics.GenericAPIView):
#     serializer_class = PasswordResetConfirmSerializer

#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         new_password = serializer.validated_data['new_password1']

#         # Set the new password
#         user.set_password(new_password)
#         user.save()

#         # Return a success response
#         return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

#     def get_serializer(self, *args, **kwargs):
#         """
#         Override get_serializer method to pass request context to serializer
#         """
#         kwargs['context'] = self.get_serializer_context()
#         return self.serializer_class(*args, **kwargs)

#     def get_serializer_context(self):
#         """
#         Override get_serializer_context to include request in context
#         """
#         return {'request': self.request}


# class SubUserLoginView(generics.CreateAPIView, MyTokenObtainPairView):
#     serializer_class = SubUserLoginSerializer
#     permission_classes = [IsAdminUser]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         try:
#             serializer.is_valid(raise_exception=True)
#         except TokenError as e:
#             raise InvalidToken(e.args[0])

#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
    

# class SubUserRegisterView(generics.CreateAPIView, MyTokenObtainPairView):
#     serializer_class = SubUserRegisterSerializer
#     permission_classes = [IsAdminUser]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         refresh = RefreshToken.for_user(user)
#         res = {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }

#         return Response({
#             "user": serializer.data,
#             "refresh": res["refresh"],
#             "token": res["access"]
#         }, status=status.HTTP_201_CREATED)