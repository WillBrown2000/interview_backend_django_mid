from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderListByDateView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        embargo_date = self.request.query_params.get('embargo_date', None)

        if start_date and embargo_date:
            try:
                queryset = queryset.filter(created_at__gte=start_date, created_at__lte=embargo_date)
            except ValueError:
                raise ValidationError('Invalid date format. Use YYYY-MM-DD.')
        
        return queryset