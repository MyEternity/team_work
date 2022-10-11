from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import UserProfile

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['username'].label = 'Пользователь'
        self.fields['password'].label = 'Пароль'

    class Meta:
        model = User
        fields = ('username', 'password')


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

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True


class UserProfileForm(forms.ModelForm):
    avatar_image = forms.ImageField(widget=forms.FileInput(), required=False)
    profile_image = forms.ImageField(widget=forms.FileInput(), required=False)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('userid',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].widget.attrs['placeholder'] = 'Дата рождения'
        self.fields['gender'].widget.attrs['placeholder'] = 'Гендер'
        self.fields['about'].widget.attrs['placeholder'] = 'О себе'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Номер телефона'
        for field_name, field in self.fields.items():
            if field_name == 'gender':
                field.widget.attrs['class'] = 'form-control'
            elif field_name != 'phone_number':
                field.widget.attrs['class'] = 'form-control py-4'
        for field in (self.fields['avatar_image'], self.fields['profile_image']):
            field.widget.attrs['class'] = 'custom-file-input'
