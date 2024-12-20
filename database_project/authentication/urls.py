from django.urls import path
from .views import (
    LandingView,
    LoginView,
    RegisterView,
    ChangePasswordView,
    LogoutView,
    MyCoursesView,
    AllCoursesView,
    ScheduleView,
    CourseDetailView,
    EnrollView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('my_courses/', MyCoursesView.as_view(), name='my_courses'),
    path('all_courses/', AllCoursesView.as_view(), name='all_courses'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('course_detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('enroll/<int:course_id>/', EnrollView.as_view(), name='enroll'),

    # Set my_courses as default after login
    path('', LandingView.as_view(), name='home'),
]
