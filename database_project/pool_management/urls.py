from django.urls import path
from pool_management.views import PoolLaneSlotBookingView
from pool_management.views import BookedPoolLaneSlotsView

urlpatterns = [
    path('pool_lane_slot_booking/', PoolLaneSlotBookingView.as_view(), name='pool_slot_booking'),
    path('booked_pool_lane_slots/', BookedPoolLaneSlotsView.as_view(), name='booked_slots'),
]
