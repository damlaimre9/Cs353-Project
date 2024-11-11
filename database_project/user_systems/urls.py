from django.urls import path
from user_systems.views import AdminHomeView
from user_systems.views import AdminProfileView
from user_systems.views import CoachHomeView
from user_systems.views import CoachProfileView
from user_systems.views import LifeguardHomeView
from user_systems.views import LifeguardProfileView
from user_systems.views import MemberHomeView
from user_systems.views import MemberProfileView
from user_systems.views import MemberRankingListView
from user_systems.views import NonmemberHomeView
from user_systems.views import NonmemberProfileView
from user_systems.views import ScheduleView

urlpatterns = [
    path('admin_home/', AdminHomeView.as_view(), name='admin_home'),
    path('admin_profile/', AdminProfileView.as_view(), name='admin_profile'),
    path('coach_home/', CoachHomeView.as_view(), name='coach_home'),
    path('coach_profile/', CoachProfileView.as_view(), name='coach_profile'),
    path('lifeguard_home/', LifeguardHomeView.as_view(), name='lifeguard_home'),
    path('lifeguard_profile/', LifeguardProfileView.as_view(), name='lifeguard_profile'),
    path('member_home/', MemberHomeView.as_view(), name='member_home'),
    path('member_profile/', MemberProfileView.as_view(), name='member_profile'),
    path('member_ranking/', MemberRankingListView.as_view(), name='member_ranking'),
    path('nonmember_home/', NonmemberHomeView.as_view(), name='nonmember_home'),
    path('nonmember_profile/', NonmemberProfileView.as_view(), name='nonmember_profile'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),    
]
