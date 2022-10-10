from django.urls import path

from .views import IndexView, RegisterUser, LoginUser, logout_user

app_name = 'users'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('authorization', LoginUser.as_view(), name='authorization'),
    path('logout', logout_user, name='logout'),
    path('registration', RegisterUser.as_view(), name='registration'),
]
