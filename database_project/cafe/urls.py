from django.urls import path
from cafe.views import CafeItemsView
from cafe.views import PurchaseItemView
from cafe.views import PreviousPurchasesView

urlpatterns = [
    path('cafe_items/', CafeItemsView.as_view(), name='cafe_items'),
    path('purchase_item/', PurchaseItemView.as_view(), name='purchase_item'),
    path('previous_purchases/', PreviousPurchasesView.as_view(), name='previous_purchases'),
]
