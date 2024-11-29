from django import forms
from django.contrib.auth.models import User
from design_pro.main.models import UserProfile, cyrillic_validator, latin_validator, \
    email_validator  # Абсолютный импорт
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError

# Валидаторы (из models.py)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    agreed_to_terms = forms.BooleanField(required=True, verbose_name='Согласие на обработку данных')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
        }

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not cyrillic_validator(data) or not data:
           raise ValidationError('Поле должно содержать только кириллицу, пробелы и дефисы. Обязательно для заполнения.')
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not cyrillic_validator(data) or not data:
           raise ValidationError('Поле должно содержать только кириллицу, пробелы и дефисы. Обязательно для заполнения.')
        return data

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username or not latin_validator(username):
            raise ValidationError('Поле должно содержать только латиницу и дефисы. Обязательно для заполнения.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email or not email_validator(email):
            raise ValidationError('Введите корректный email. Обязательно для заполнения.')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('title', 'category', 'plan', 'description')