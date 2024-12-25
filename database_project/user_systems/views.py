from django.shortcuts import render
from django.db import connection
from django.views import View


class AdminHomeView(View):
    template_name = 'user_systems/admin_home_page.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class AdminProfileView(View):
    template_name = 'user_systems/admin_profile.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class CoachHomeView(View):
    template_name = 'user_systems/coach_home_page.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class CoachProfileView(View):
    template_name = 'user_systems/coach_profile.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class LifeguardHomeView(View):
    template_name = 'user_systems/lifeguard_home_page.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class LifeguardProfileView(View):
    template_name = 'user_systems/lifeguard_profile.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)  

class MemberHomeView(View):
    template_name = 'user_systems/member_home_page.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class MemberProfileView(View):
    template_name = 'user_systems/member_profile.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class MemberRankingListView(View):
    template_name = 'user_systems/member_ranking_list.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class NonmemberHomeView(View):
    template_name = 'user_systems/non_member_home_page.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class NonmemberProfileView(View):
    template_name = 'user_systems/non_member_profile.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class ScheduleView(View):
    template_name = 'user_systems/schedule.html' 
    def get(self, request, *args, **kwargs):
        if 'user_id' not in request.session:
            return render(request, 'authentication/login.html')
          
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