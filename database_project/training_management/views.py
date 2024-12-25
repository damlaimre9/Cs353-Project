from django.shortcuts import render
from django.db import connection
from django.views import View

class CourseInformationView(View):
    template_name = 'training_management/course_information.html' 

    def get(self, request, course_id):
        if 'user_id' not in request.session:
            return render(request, 'authentication/login.html')

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
    
class CourseListView(View):
    template_name = 'training_management/course_list.html' 

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return render(request, 'authentication/login.html')

        user_id = request.session['user_id']
        search_query = request.GET.get('search', '')
        filter_option = request.GET.get('filter', 'all') # 'all', 'enrolled', 'not_enrolled'

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
            conditions.append("""
                c.course_id IN (
                    SELECT course_id FROM course_schedule WHERE swimmer_id = %s
                )
            """)
            params.append(user_id)
        elif filter_option == 'not_enrolled':
            conditions.append("""
                c.course_id NOT IN (
                    SELECT course_id FROM course_schedule WHERE swimmer_id = %s
                )
            """)
            params.append(user_id)
    
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


class CreateCourseView(View):
    template_name = 'training_management/create_course.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class EnrollCourseView(View):
    template_name = 'training_management/enroll_course.html' 
     
    def get(self, request, course_id):
        if 'user_id' not in request.session:
            return render(request, 'authentication/login.html')

        user_id = request.session['user_id']

        # Check if already enrolled
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM course_schedule WHERE swimmer_id=%s AND course_id=%s", [user_id, course_id])
            already = cursor.fetchone()

        if already:
            # User is already enrolled
            return render(request, 'training_management/my_courses.html')

        # Fetch the course details
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT coach_id, deadline
                FROM course
                WHERE course_id=%s
            """, [course_id])
            course_details = cursor.fetchone()

        if not course_details:
            return render(request, 'training_management/course_list.html')

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

        return render(request, 'training_management/my_courses.html')

class MyCoursesView(View):
    template_name = 'training_management/my_courses.html' 

    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return render(request, 'authentication/login.html')

        user_id = request.session['user_id']

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT c.course_name
                FROM course_schedule cs
                JOIN course c ON cs.course_id = c.course_id
                WHERE cs.swimmer_id = %s
            """, [user_id])
            enrolled_courses = cursor.fetchall()

        return render(request, self.template_name, {'enrolled_courses': enrolled_courses})

class PreviousCoursesView(View):
    template_name = 'training_management/previous_courses.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
