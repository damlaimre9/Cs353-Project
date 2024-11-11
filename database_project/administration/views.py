from django.shortcuts import render
from django.views import View
from django.db import connection

class DataAnalysisView(View):
    template_name = 'administration/data_analysis.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class PoolUsersInfoView(View):
    template_name = 'administration/pool_users_info.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class PoolWorkersInfoView(View):
    template_name = 'administration/pool_workers_info.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class ReportArchiveView(View):
    template_name = 'administration/report_archive.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    