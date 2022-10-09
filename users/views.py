from django.views.generic import FormView


# Create your views here.


class IndexView(FormView):
    title = '#Заглушка#'
    form_class = FormView
    template_name = 'users/default.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class AuthorizationView(FormView):
    title = 'Authorization'
    form_class = FormView
    template_name = 'users/authorization.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)
        return context


class RegistrationView(FormView):
    title = 'Registration'
    form_class = FormView
    template_name = 'users/registration.html'

    def get_context_data(self, **kwargs):
        context = super(RegistrationView, self).get_context_data(**kwargs)
        return context
