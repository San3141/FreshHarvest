from decimal import Decimal
from gettext import translation
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Discount, Order, OrderItem, Product, Cart, CartItem
from .serializers import CartSerializer
from django.db import transaction
from django.utils.timezone import now

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        # Only show the user's carts
        return Cart.objects.filter(user=self.request.user)

    def get_active_cart(self, user):
        # Get or create active cart for the logged-in user
        cart, _ = Cart.objects.get_or_create(user=user, status="active")
        return cart

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart = self.get_active_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or not quantity:
            return Response({"error": "Both product_id and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantity must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart = self.get_active_cart(request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            farmer=product.farmer,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_active_cart(request.user)

        try:
            cart_item = cart.items.get(product_id=product_id)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def decrease_quantity(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({"error": "Quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantity must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        cart = self.get_active_cart(request.user)

        try:
            cart_item = cart.items.get(product_id=product_id)
            if cart_item.quantity > quantity:
                cart_item.quantity -= quantity
                cart_item.save()
                return Response({"message": "Quantity decreased"}, status=status.HTTP_200_OK)
            else:
                cart_item.delete()
                return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)
        


    @action(detail=False, methods=['post'])
    @transaction.atomic
    def checkout(self, request):
        cart = Cart.objects.filter(user=request.user, status="active").first()
        if not cart or not cart.items.exists():
            return Response({"error": "Cart is empty or does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        

        total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
        discount_amount = Decimal(0.0)

        discount_code = request.data.get("discount_code")
        if discount_code:
            try:
                discount = Discount.objects.get(discount_code=discount_code)
                discount_amount = discount.value
                total_amount -= total_amount * discount_amount
                if total_amount <0:
                    total_amount = Decimal(0.0)
            except Discount.DoesNotExist:
                return Response({"error": "Not a valid discount code"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_amount= total_amount,
            mode_payment=request.data.get("mode_payment", "cash"),
            delivery_date=request.data.get("delivery_date"),
            delivery_address=request.data.get("delivery_address", ""),
            order_date=now().date()
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price_kg
            )

        cart.items.all().delete()
        cart.status = "checked_out"
        cart.save()

        return Response({"message": "Checkout successful", "order_id": order.id}, status=status.HTTP_201_CREATED)