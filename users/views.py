from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserForm, UserProfileForm
from users.models import User
from articles.models import Article
from common.views import CommonContextMixin


# Аутентификация пользователя
class AuthorizationView(CommonContextMixin, LoginView):
    title = 'Authorization'
    form_class = UserLoginForm
    template_name = 'users/authorization.html'


# Регистрация пользователя
class RegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    title = 'Registration'
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:authorization')
    success_message = 'You have successfully registered'


# Профиль
class UserProfileView(CommonContextMixin, UpdateView, SuccessMessageMixin):
    model = User
    title = 'Profile'
    form_class = UserForm
    template_name = 'users/lk_users.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile'] = UserProfileForm(instance=self.request.user.userprofile)
        context['articles'] = Article.objects.filter(author_id=self.request.user.id)
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = UserForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            messages.success(self.request, 'Данные успешно обновлены!')
            form.save()
        else:
            messages.warning(self.request, 'Что-то пошло не так')
        return redirect(self.success_url)


class UserLogoutView(LogoutView):
    pass
