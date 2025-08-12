from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


from .models import Cart, CartItem, Order, OrderItem, Product
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user = self.request.user).order_id('-id')  #to get the most recent orders first






    # def create(self, request, *args, **kwargs):
    #     user = request.user
        
    #     cart = Cart.objects.filter(user= user, status='active').first()
    #     if not cart:
    #         return Response({"error":"No active Cart"}, status= status.HTTP_400_BAD_REQUEST)
        
    #     cart_item = CartItem.objects.filter(cart=cart)
    #     if not cart_item:
    #         return Response({"error":"The Cart is empty"}, status= status.HTTP_400_BAD_REQUEST)
        
    #     total_amount =0
    #     for item in cart_item:
    #         total_amount += item.product.price * item.quantity

    #     order = Order.objects.create(
    #         user=user,
    #         cart=cart,
    #         total_amount=total_amount,
    #         mode_payment=request.data.get("mode_payment", "COD"),  # Default: Cash on Delivery
    #         delivery_date=request.data.get("delivery_date"),
    #         delivery_address=request.data.get("delivery_address", ""),
    #         order_date=now().date()

    #     )


    #     order_items = []
    #     for item in cart_item:
    #         order_items.append(OrderItem(
    #             order=order,
    #             product=item.product,
    #             quantity=item.quantity
    #         ))