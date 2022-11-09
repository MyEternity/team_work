from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('public_profile/<int:pk>/', PublicUserProfileView.as_view(), name='public_profile'),
    path('verify/<str:email>/<str:activate_key>/', RegistrationView.verify, name='verify'),
    path('block_user/<int:pk>/', BlockUserView.as_view(), name='block'),
]
