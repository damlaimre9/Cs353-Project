from django.urls import path
from rating_system.views import CoachRatingsView
from rating_system.views import PersonalTrainingRatingsView
from rating_system.views import CourseRatingsView

urlpatterns = [
    path('course_ratings/', CourseRatingsView.as_view(), name='course_ratings'),
    path('coach_ratings/', CoachRatingsView.as_view(), name='coach_ratings'),
    path('coach_ranking/', CoachRatingsView.as_view(), name='coach_rankings'),
    path('personal_training_ratings/', PersonalTrainingRatingsView.as_view(), name='personal_training_ratings'),
]
