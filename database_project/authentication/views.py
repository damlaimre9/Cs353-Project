
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.urls import reverse

class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", [username, password])
            user = cursor.fetchone()

        if user:
            # user is a tuple like (user_id,)
            request.session['user_id'] = user[0]
            return redirect('my_courses')  # after login go to my_courses page
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})


class RegisterView(View):
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        user_type = request.POST.get('user-type')  # you may or may not use this

        # Check if username exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE username=%s", [username])
            existing = cursor.fetchone()

        if existing:
            return render(request, self.template_name, {'error': 'Username already taken'})

        # Insert new user
        # Assuming user_id is auto-increment in db:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (forename, surname, username, password, account_money)
                VALUES (%s, %s, %s, %s, 0)
                RETURNING user_id
            """, [name, surname, username, password])
            new_user_id = cursor.fetchone()[0]

        return redirect('login')


class ChangePasswordView(View):
    template_name = 'authentication/change_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        old_password = request.POST.get('password')
        new_password = request.POST.get('new-password')

        with connection.cursor() as cursor:
            # Check if user exists with old password
            cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", [username, old_password])
            user = cursor.fetchone()

        if user:
            # Update password
            with connection.cursor() as cursor:
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", [new_password, username])
            return redirect('login')
        else:
            return render(request, self.template_name, {'error': 'Invalid username or old password'})


class LogoutView(View):
    def get(self, request):
        request.session.flush()  # Clear session
        return redirect('login')

