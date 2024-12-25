
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.shortcuts import redirect
 
class LoginView(View):
    template_name = 'authentication/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM all_users WHERE username=%s AND password=%s", [username, password])
            user = cursor.fetchone()
            print(user)
            
        if user is not None: 
            user_id = user[0]
            request.session['user_id'] = user_id

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM member_swimmer WHERE swimmer_id=%s", [user_id])
                swimmer = cursor.fetchone()
                if swimmer:
                    return render(request, 'user_systems/member_home_page.html', {'user_id': user_id})
                
                cursor.execute("SELECT * FROM coach WHERE coach_id=%s", [user_id])
                coach = cursor.fetchone()
                if coach:
                    return render(request, 'user_systems/coach_home_page.html', {'user_id': user_id})

                cursor.execute("SELECT * FROM lifeguard WHERE lifeguard_id=%s", [user_id])
                lifeguard = cursor.fetchone()
                if lifeguard:
                    return render(request, 'user_systems/lifeguard_home_page.html', {'user_id': user_id})
                
                cursor.execute("SELECT * FROM administrator WHERE administrator_id=%s", [user_id])
                admin = cursor.fetchone()
                if admin:
                    return render(request, 'user_systems/admin_home_page.html', {'user_id': user_id})
    
                else:
                    return render(request, 'user_systems/non_member_home_page.html', {'user_id': user_id})
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})


class RegisterView(View):
    template_name = 'authentication/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        
    def post(self, request):
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        user_type = request.POST.get('user-type')

        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM all_users WHERE username=%s", [username])
            existing = cursor.fetchone()

        if existing:
            return render(request, self.template_name, {'error': 'Username already taken'})

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO all_users (forename, surname, username, password, account_money)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id
            """, [name, surname, username, password, 0])
            new_user_id = cursor.fetchone()[0]

        if new_user_id and user_type == "1":  # Swimmer
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO swimmer (swimmer_id, phone_number, age, gender, swimming_proficiency, number_of_booked_slots, total_courses_enrolled, total_courses_terminated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [new_user_id, "", 0, "", "", 0, 0, 0]) 
                
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO nonmember_swimmer (swimmer_id, registration_timestamp)
                    VALUES (%s, CURRENT_TIMESTAMP)
                """, [new_user_id])
                
        elif new_user_id and  user_type == "3":  # Lifeguard
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO worker (worker_id, pool_id, salary, age, gender, phone_number, swim_proficiency, qualifications)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [new_user_id, 0, 0, 0, "", "", "", ""])

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO lifeguard (lifeguard_id, certifications)
                    VALUES (%s, %s)
                """, [new_user_id, ""])  

        elif new_user_id and user_type == "4":  # Coach
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO worker (worker_id, pool_id, salary, age, gender, phone_number, swim_proficiency, qualifications)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [new_user_id, 0, 0, 0, "", "", "", ""]) 

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO coach (coach_id, avg_rating, coach_ranking, specialties)
                    VALUES (%s, %s, %s, %s)
                """, [new_user_id, 0, 0, ""])

        elif new_user_id and  user_type == "5":  # Administrator
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO administrator (administrator_id, number_of_reports)
                    VALUES (%s, %s)
                """, [new_user_id, 0]) 

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
            cursor.execute("SELECT user_id FROM all_users WHERE username=%s AND password=%s", [username, old_password])
            user = cursor.fetchone()

        if user:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE all_users SET password=%s WHERE username=%s", [new_password, username])
            return redirect('login')
        else:
            return render(request, self.template_name, {'error': 'Invalid username or old password'})


class LogoutView(View):
    def get(self, request):
        request.session.flush() 
        return redirect('login')
