
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime, timedelta

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
class MyCoursesView(View):
    template_name = 'authentication/my_courses.html'

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')

        user_id = request.session['user_id']

        # Fetch user’s courses
        # We join course_schedule and course to get course_name
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name
                FROM course_schedule cs
                JOIN course c ON cs.course_id = c.course_id
                WHERE cs.swimmer_id = %s
            """, [user_id])
            enrolled_courses = cursor.fetchall()

        # enrolled_courses is a list of tuples [(course_name,), (course_name2,)...]
        return render(request, self.template_name, {'enrolled_courses': enrolled_courses})
    
class AllCoursesView(View):
    template_name = 'authentication/all_courses.html'

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')

        user_id = request.session['user_id']
        search_query = request.GET.get('search', '')
        filter_option = request.GET.get('filter', 'all') # 'all', 'enrolled', 'not_enrolled'

        # Build the SQL based on filters
        base_sql = """
            SELECT c.course_id, c.course_name, c.coach_id
            FROM course c
        """

        conditions = []
        params = []

        if search_query:
            conditions.append("c.course_name ILIKE %s")
            params.append('%' + search_query + '%')

        if filter_option == 'enrolled':
            # courses where user is enrolled
            conditions.append("""
                c.course_id IN (
                    SELECT course_id FROM course_schedule WHERE swimmer_id = %s
                )
            """)
            params.append(user_id)
        elif filter_option == 'not_enrolled':
            # courses where user is not enrolled
            conditions.append("""
                c.course_id NOT IN (
                    SELECT course_id FROM course_schedule WHERE swimmer_id = %s
                )
            """)
            params.append(user_id)
        # if 'all', no extra condition

        if conditions:
            base_sql += " WHERE " + " AND ".join(conditions)

        with connection.cursor() as cursor:
            cursor.execute(base_sql, params)
            courses = cursor.fetchall()

        return render(request, self.template_name, {
            'courses': courses,
            'search_query': search_query,
            'filter_option': filter_option,
        })

class CourseDetailView(View):
    template_name = 'authentication/course_detail.html'

    def get(self, request, course_id):
        if 'user_id' not in request.session:
            return redirect('login')

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT course_name, course_description, deadline, pool_id, lane_id, price, coach_id
                FROM course
                WHERE course_id=%s
            """, [course_id])
            course = cursor.fetchone()

        if not course:
            return render(request, self.template_name, {'error': 'Course not found'})

        # course is a tuple (course_name, description, deadline, pool_id, lane_id, price, coach_id)
        return render(request, self.template_name, {
            'course_id': course_id,
            'course_name': course[0],
            'course_description': course[1],
            'deadline': course[2],
            'pool_id': course[3],
            'lane_id': course[4],
            'price': course[5],
            'coach_id': course[6],
        })

class EnrollView(View):
    def get(self, request, course_id):
        if 'user_id' not in request.session:
            return redirect('login')

        user_id = request.session['user_id']

        # Check if already enrolled
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM course_schedule WHERE swimmer_id=%s AND course_id=%s", [user_id, course_id])
            already = cursor.fetchone()

        if already:
            # User is already enrolled
            return redirect('my_courses')

        # Fetch the course details
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT coach_id, deadline
                FROM course
                WHERE course_id=%s
            """, [course_id])
            course_details = cursor.fetchone()

        if not course_details:
            # Invalid course ID
            return redirect('all_courses')

        coach_id, deadline = course_details

        # Set default start_date, end_date, start_time, end_time, and day
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=30)
        start_time = datetime.now().time().replace(hour=9, minute=0, second=0)  # Default to 9:00 AM
        end_time = datetime.now().time().replace(hour=10, minute=0, second=0)  # Default to 10:00 AM
        day = 'Monday'  # Default to Monday; you can adjust based on requirements

        # Insert the new enrollment
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO course_schedule (
                    course_id, swimmer_id, coach_id, start_date, end_date, start_time, end_time, day
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [course_id, user_id, coach_id, start_date, end_date, start_time, end_time, day])

        # Redirect to 'My Courses'
        return redirect('my_courses')
class ScheduleView(View):
    template_name = 'authentication/schedule.html'

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')

        user_id = request.session['user_id']

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name, cs.start_date, cs.end_date
                FROM course_schedule cs
                JOIN course c ON cs.course_id = c.course_id
                WHERE cs.swimmer_id = %s
            """, [user_id])
            courses = cursor.fetchall()

        # courses: [(course_name, start_date, end_date), ...]

        return render(request, self.template_name, {'courses': courses})

class LandingView(View):
    def get(self, request, *args, **kwargs):
        # Check if the user is authenticated by checking if 'user_id' is in session
        if 'user_id' in request.session:
            return redirect('my_courses')  # Redirect to 'My Courses' if logged in
        else:
            return redirect('login')  # Redirect to login page otherwise
