from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Customer, Farmer, Product, Review, Discount, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        product = get_object_or_404(self.queryset, pk=product_id)
        serializer = self.get_serializer(product)
        return Response(serializer.data)