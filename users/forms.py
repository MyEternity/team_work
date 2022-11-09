import datetime
import hashlib
import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from users.models import User
from users.models import UserProfile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    error_messages = {
        **AuthenticationForm.error_messages,
        "blocked": (
            "Пользователь %(username)s заблокирован за нарушение правил до %(date)s"
        ),
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['username'].label = 'Пользователь'
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = User
        fields = ('username', 'password')

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.blocked_until > datetime.date.today():
            raise ValidationError(
                self.error_messages["blocked"],
                code="blocked",
                params={"username": user.username,
                        "date": user.blocked_until},
            )


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Придумайте логин'
        self.fields['username'].label = 'Пользователь'
        self.fields['email'].widget.attrs['placeholder'] = 'myemail@mail.ml'
        self.fields['email'].label = 'Электронная почта'
        self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        self.fields['password2'].label = 'Повторите пароль'

    def save(self):
        # метод дополнительно создает ключ активации пользователя
        user = super(UserRegistrationForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf-8')).hexdigest()
        user.save()
        return user


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = \
            'Введите ваше имя'
        self.fields['last_name'].widget.attrs['placeholder'] = \
            'Введите вашу фамилию'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True


class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput(), required=False)
    birthday = forms.DateField(widget=forms.DateInput(), required=False)
    about = forms.CharField(widget=forms.Textarea(), required=False)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('userid',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget.attrs['placeholder'] = \
            'Введите дату рождения'
        self.fields['about'].widget.attrs['placeholder'] = \
            'Введите что-нибудь о себе'
        self.fields['phone_number'].widget.attrs['placeholder'] = \
            'Номер телефона'
