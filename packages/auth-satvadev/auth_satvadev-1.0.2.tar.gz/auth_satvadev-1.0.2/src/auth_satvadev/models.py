from django.contrib.auth import get_user_model
from django.db import models


class VerificationCode(models.Model):
    """Модель хранит email пользователя и проверочный код"""
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    code = models.PositiveIntegerField()

    def __str__(self):
        """Строковое представление кодов подтверждения"""
        return f'VerificationCode #{self.id}, Code {self.code}'
