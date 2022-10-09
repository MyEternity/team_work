from django.urls import path

from .views import IndexView, AuthorizationView, RegistrationView

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('authorization', AuthorizationView.as_view(), name='authorization'),
    path('registration', RegistrationView.as_view(), name='registration'),
]
