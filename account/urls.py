from django.urls import path, include
from .views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from . import views  
from django.contrib.auth import views as auth_views



router = DefaultRouter()
router.register(r'users', UserViewSet),
<<<<<<< HEAD
=======
# router.register("user", views.UserViewSet, basename="user"),
# router.register("registre", views.UserRegistrationView, basename="register"),
>>>>>>> 9760532483ae95be0ec254447b44854be07497bf

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', UserRegistrationView.as_view({'post': 'register'}), name='register'),
<<<<<<< HEAD
    # path('', include(router.urls), name='user-list'),
=======
    # path('verify_otp/', UserViewSet.as_view({'patch': 'verify_otp'}), name='verify_otp'),
    # path('profile_update/', UserViewSet.as_view({'patch': 'profile_update'}), name='profile_update'),
    # path('regenerate_otp/', UserViewSet.as_view({'post': 'regenerate_otp'}), name='regenerate_otp'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include(router.urls), name='user-list'),
>>>>>>> 9760532483ae95be0ec254447b44854be07497bf
]
urlpatterns += router.urls