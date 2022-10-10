from django.views.generic import FormView

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth import logout

from .forms import LoginUserForm, RegisterUserForm


class IndexView(FormView):
    title = '#Заглушка#'
    form_class = FormView
    template_name = 'users/default.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


# class AuthorizationView(FormView):
#     title = 'Authorization'
#     form_class = FormView
#     template_name = 'users/authorization.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(AuthorizationView, self).get_context_data(**kwargs)
#         return context


# class RegistrationView(FormView):
#     title = 'Registration'
#     form_class = FormView
#     template_name = 'users/registration.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(RegistrationView, self).get_context_data(**kwargs)
#         return context

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:authorization')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/authorization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')
