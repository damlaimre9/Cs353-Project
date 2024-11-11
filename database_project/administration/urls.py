from django.urls import path
from administration.views import DataAnalysisView
from administration.views import PoolUsersInfoView
from administration.views import PoolWorkersInfoView
from administration.views import ReportArchiveView

urlpatterns = [
    path('data_analysis/', DataAnalysisView.as_view(), name='data_analysis'),
    path('pool_users/', PoolUsersInfoView.as_view(), name = 'pool_users'),
    path('pool_workers/', PoolWorkersInfoView.as_view(), name='pool_workers'),
    path('reports_archive/', ReportArchiveView.as_view(), name='report_archive'),
]
