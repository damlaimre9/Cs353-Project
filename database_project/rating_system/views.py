from django.shortcuts import render
from django.views import View
from django.db import connection

class CourseRatingsView(View):
    template_name = 'rating_system/course_ratings.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class PersonalTrainingRatingsView(View):
    template_name = 'rating_system/personal_training_ratings.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class CoachRatingsView(View):
    template_name = 'rating_system/coach_ratings.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class CoachRankingView(View):
    template_name = 'rating_system/coach_rankings.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   