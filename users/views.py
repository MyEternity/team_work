from django.views.generic import FormView


# Create your views here.


class IndexView(FormView):
    title = '#Заглушка#'
    form_class = FormView
    template_name = 'users/default.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
