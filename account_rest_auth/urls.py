from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views  
from django.contrib.auth import views as auth_views
from .views import (
    LoginView, LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)


urlpatterns = [
    path('password/reset/', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
<<<<<<< HEAD
    # path('login/', LoginView.as_view(), name='rest_login'),
=======
    path('login/', LoginView.as_view(), name='rest_login'),
>>>>>>> 9760532483ae95be0ec254447b44854be07497bf
    # paths that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(),
        name='rest_password_change'),
]