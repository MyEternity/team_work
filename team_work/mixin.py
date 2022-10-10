from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseNotAllowed
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import ContextMixin


class UserIsAdminCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserIsAdminCheckMixin, self).dispatch(request, *args, **kwargs)


class UserLoginCheckMixin(View):
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            if request.user.is_staff:
                return super(UserLoginCheckMixin, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponseNotAllowed(request.method)
        else:
            return HttpResponseNotAllowed(request.method)


class BaseClassContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(BaseClassContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context
