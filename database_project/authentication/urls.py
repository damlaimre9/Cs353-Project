from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    ChangePasswordView,
    LogoutView,
)
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
