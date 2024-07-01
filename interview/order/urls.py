
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderListByDateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('orders/date-range/', OrderListByDateView.as_view(), name='order-list-by-date'),

]