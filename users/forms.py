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
        self.fields['first_name'].widget.attrs['placeholder'] = \
            'Введите ваше имя'
        self.fields['last_name'].widget.attrs['placeholder'] = \
            'Введите вашу фамилия'
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'


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
            'Введите что нибудь о себе'
        self.fields['phone_number'].widget.attrs['placeholder'] = \
            'Номер телефона - в формате 89123456789'
