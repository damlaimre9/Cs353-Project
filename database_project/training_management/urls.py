from django.urls import path
from training_management.views import CourseInformationView
from training_management.views import CourseListView
from training_management.views import CreateCourseView
from training_management.views import EnrollCourseView
from training_management.views import MyCoursesView
from training_management.views import PreviousCoursesView

urlpatterns = [
    path('course_info/', CourseInformationView.as_view(), name='course_info'),
    path('course_list/', CourseListView.as_view(), name='course_list'),
    path('create_course/', CreateCourseView.as_view(), name='create_course'),
    path('enroll_course/', EnrollCourseView.as_view(), name='enroll_course'),
    path('my_courses/', MyCoursesView.as_view(), name='my_courses'),
    path('previous_courses/', PreviousCoursesView.as_view(), name='previous_courses'),
]
