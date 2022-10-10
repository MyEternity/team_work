from django.views.generic import FormView

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm # UserProfileForm
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


"""
# Профиль
class UserProfileView(CommonContextMixin, UpdateView):
    model = User
    title = 'Profile'
    form_class = UserProfileForm
    template_name = 'users/lk_users.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(user=self.object)
        return context

"""


class UserLogoutView(LogoutView):
    pass
