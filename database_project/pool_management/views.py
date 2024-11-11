from django.shortcuts import render
from django.db import connection
from django.views import View

class PoolLaneSlotBookingView(View):
    template_name = 'pool_management/pool_lane_slot_booking.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   

class BookedPoolLaneSlotsView(View):
    template_name = 'pool_management/booked_pool_lane_slots.html' 
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)   
