from django import forms
from django.contrib.auth.models import User

from .utils import send_welcome_email


class RegisterForm(forms.ModelForm):
    # создаем модельки, которые нету в форме user'a
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation')

    # валидация и подтверждение пароля
    def clean(self):
        data = self.cleaned_data
        # data = {'password': 'qwerty', 'password_confirmation': 'qwerty'}
        password = data.get('password')
        password_conf = data.pop('password_confirmation')
        if password != password_conf:
            raise forms.ValidationError('Passwords do not match!')
        return data

    # валидация email'а и если есть вернуть ошибку
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():   # exists() - возвращает только true или false (есть такой email или нет)
            raise forms.ValidationError('User with such email already exists!')
        return email

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        send_welcome_email(user.email)
        return user
