from django.shortcuts import render
from django.views import View
from django.db import connection

class LoginView(View):
    template_name = 'authentication/login.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class RegisterView(View):
    template_name = 'authentication/register.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class ChangePasswordView(View):
    template_name = 'authentication/change_password.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
