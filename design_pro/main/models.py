from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

# Валидаторы
cyrillic_validator = RegexValidator(r'^[\u0400-\u04FF\s\-]+', 'Только кириллица, пробелы и дефисы.')
latin_validator = RegexValidator(r'^[a-zA-Z\-]+$', 'Только латиница и дефисы.')
email_validator = EmailValidator()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, validators=[cyrillic_validator], verbose_name='ФИО')
    agreed_to_terms = models.BooleanField(default=False, verbose_name='Согласие на обработку данных')

    def __str__(self):
        return self.user.username

    def clean(self):
        if not self.full_name:
           raise ValidationError('ФИО обязательно для заполнения.')

    def save(self, *args, **kwargs):
        self.full_name = self.full_name()
        super().save(*args, **kwargs)


class Request(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
        ('pending', 'Ожидает обработки'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    category = models.CharField(max_length=255, verbose_name='Категория')
    plan = models.FileField(upload_to='plans/', verbose_name='План помещения')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name