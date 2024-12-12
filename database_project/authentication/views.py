
from django.db import connection

#class LoginView(View):
 #   template_name = 'authentication/login.html' 
  #  def get(self, request, *args, **kwargs):
   #     return render(request, self.template_name)   

#class RegisterView(View):
 #   template_name = 'authentication/register.html' 
  #  def get(self, request, *args, **kwargs):
   #     return render(request, self.template_name)   

#class ChangePasswordView(View):
 #   template_name = 'authentication/change_password.html' 
  #  def get(self, request, *args, **kwargs):
   #     return render(request, self.template_name)  
    
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.urls import reverse
from .models import User

class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if user exists
            user = User.objects.get(username=username, password=password)
            # Set session
            request.session['user_id'] = user.user_id
            return redirect('main')
        except User.DoesNotExist:
            # User not found or wrong password
            return render(request, self.template_name, {
                'error': 'Invalid username or password'
            })


class RegisterView(View):
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        user_type = request.POST.get('user-type')  # If provided

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {
                'error': 'Username already taken'
            })

        # Create new user
        user = User.objects.create(
            username=username,
            forename=name,
            surname=surname,
            password=password,
            account_money=0.00,
            # user_type=user_type if you have this field
        )

        # After registration, user can be redirected to login page
        return redirect('login')


class ChangePasswordView(View):
    template_name = 'authentication/change_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        old_password = request.POST.get('password')
        new_password = request.POST.get('new-password')

        try:
            user = User.objects.get(username=username, password=old_password)
            user.password = new_password
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request, self.template_name, {
                'error': 'Invalid username or old password'
            })

class MainView(View):
    template_name = 'authentication/main.html'

    def get(self, request, *args, **kwargs):
        # Check if user_id is in session, if not redirect to login
        if 'user_id' not in request.session:
            return redirect('login')
        
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)
        return render(request, self.template_name, {'user': user})

