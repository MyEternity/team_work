# Create your views here.
from django.contrib import messages, auth
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings

from articles.models import Article
from team_work.mixin import BaseClassContextMixin, UserLoginCheckMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserForm, UserProfileForm
from users.models import User
from users.rating_counter import user_rating


# Аутентификация пользователя
class AuthorizationView(BaseClassContextMixin, LoginView):
    title = 'Авторизация'
    form_class = UserLoginForm
    template_name = 'users/authorization.html'


# Регистрация пользователя
class RegistrationView(BaseClassContextMixin, SuccessMessageMixin, CreateView):
    model = User
    title = 'Регистрация'
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:authorization')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_user(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request, 'Вы успешно зарегистрировались! На e-mail придет ссылка на активацию аккаунта.')
                return HttpResponseRedirect(reverse('users:authorization'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})

    def send_verify_user(self, user):
        # функция отправляет сообщение пользователю на email с ссылкой на активацию аккаунта
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} ' \
                  f' пройдите по ссылке: \n http://127.0.0.1:8000{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        # функция после проверки email и ключа активации активирует аккаунт пользователя.
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'success_registration.html')
        except Exception as err:
            return HttpResponseRedirect(reverse('articles:index'))


# Профиль
class UserProfileView(BaseClassContextMixin, UserLoginCheckMixin, UpdateView, SuccessMessageMixin):
    model = User
    title = 'Профиль'
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
        form = UserForm(data=request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, files=request.FILES, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            messages.success(self.request, 'Данные успешно обновлены!')
            form.save()
        else:
            messages.warning(self.request, 'Что-то пошло не так')
        return redirect(self.success_url)


class UserLogoutView(BaseClassContextMixin, UserLoginCheckMixin, LogoutView):
    pass


class PublicUserProfileView(BaseClassContextMixin, DetailView):
    """
    класс выводит публичный профиль пользователя
    """
    model = User
    title = 'Профиль пользователя'
    template_name = 'users/public_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(PublicUserProfileView, self).get_context_data(**kwargs)
        context['user_rating'] = user_rating(self.kwargs["pk"])  # подсчет рейтинга пользователя
        return context
