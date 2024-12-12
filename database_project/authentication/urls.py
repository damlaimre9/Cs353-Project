from django.urls import path
from authentication.views import LoginView
from authentication.views import RegisterView
from authentication.views import ChangePasswordView
from authentication.views import MainView

urlpatterns = [
    path('', LoginView.as_view(), name='login_default'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('main/', MainView.as_view(), name='main'),

]
