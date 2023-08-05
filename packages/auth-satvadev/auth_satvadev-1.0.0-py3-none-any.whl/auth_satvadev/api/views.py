from random import SystemRandom

from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_satvadev.api.serializers import (
    EmailConfirmCodeSerializer, EmailResetPasswordSerializer,
)
from auth_satvadev.models import VerificationCode

from auth_satvadev.senders import get_sender_class


class ResetPasswordView(APIView):
    """### Сброс пароля по существующему пользователю, проверяется email
    status_code: 200

    ## Exceptions
    status_code: 404
    {
        "message": "User matching query does not exist.",
        "error_code": "object_does_not_exist",
        "details": None
    }
    """
    permission_classes = [AllowAny]
    serializer_class = EmailResetPasswordSerializer
    sender_class = get_sender_class()

    def post(self, request):
        """Отправка пользователю кода подтверждения для сброса пароля"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = SystemRandom().randint(100000, 999999)
        user = serializer.data.get('user')
        VerificationCode.objects.update_or_create(
            user=user,
            defaults={
                'code': code,
            },
        )

        self.sender_class().send_code(code, serializer.data)

        return Response(status=status.HTTP_200_OK)


class ConfirmCodeView(APIView):
    """### Совпадение email и кода: если успешно - смена пароля пользователя

    status_code: 200

    ## Exceptions
    status_code: 404
    {
        "message": "User matching query does not exist.",
        "error_code": "object_does_not_exist",
        "details": None
    }

    status_code: 404
    {
        "details": null,
        "error_code": "object_does_not_exist",
        "message": "VerificationCode matching query does not exist."
    }
    """
    permission_classes = [AllowAny]
    serializer_class = EmailConfirmCodeSerializer
    sender_class = get_sender_class()

    def post(self, request):
        """Эндпоинт для валидации кода подтверждения"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.sender_class().validate_code(serializer.data)

        password = serializer.data.get('password')
        validate_password(password)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_200_OK)
