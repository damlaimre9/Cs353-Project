from django.shortcuts import render
from django.views import View
from django.db import connection

class CafeItemsView(View):
    template_name = 'cafe/cafe_items.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class PurchaseItemView(View):
    template_name = 'cafe/purchase_item.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
    
class PreviousPurchasesView(View):
    template_name = 'cafe/previous_purchases.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   