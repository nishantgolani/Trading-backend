from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views  
from django.contrib.auth import views as auth_views



router = DefaultRouter()
router.register(r'users', UserViewSet),

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', UserRegistrationView.as_view({'post': 'register'}), name='register'),
    # path('', include(router.urls), name='user-list'),
]
urlpatterns += router.urls