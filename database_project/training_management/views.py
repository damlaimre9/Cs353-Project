from django.shortcuts import render
from django.db import connection
from django.views import View

class CourseInformationView(View):
    template_name = 'training_management/course_information.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class CourseListView(View):
    template_name = 'training_management/course_list.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class CreateCourseView(View):
    template_name = 'training_management/create_course.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class EnrollCourseView(View):
    template_name = 'training_management/enroll_course.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class MyCoursesView(View):
    template_name = 'training_management/my_courses.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class PreviousCoursesView(View):
    template_name = 'training_management/previous_courses.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
