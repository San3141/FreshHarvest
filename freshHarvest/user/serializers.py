from rest_framework import serializers
from .models import Customer, Farmer, Product, Review, Discount, Cart, CartItem, Order, OrderItem

class CustomerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ReviewSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model =Review
        fields = '__all__'

class FarmerSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'

class DiscountSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'

class CartSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# nesting

class ProductSerializer(serializers.ModelSerializer):
    farmer = FarmerSimpleSerializer(read_only =True)
    reviews = ReviewSimpleSerializer(many=True, read_only = True)
    carts = CartItemSimpleSerializer(many=True, read_only= True)
    class Meta:
        model = Product
        fields = (
            'id',
            'product_name',
            'stock',
            'price',
            'harvest_date',
            'label',
            'farmer',
            'reviews',
            'carts',
        )


class FarmerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many = True, read_only = True)
    carts = CartItemSimpleSerializer(many=True, read_only= True)
    class Meta:
        model = Farmer
        fields = '__all__'



class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    reviews = ReviewSimpleSerializer(many=True, read_only = True)
    carts = CartSimpleSerializer(many=True, read_only = True)
    orders = OrderSimpleSerializer (many = True, read_only = True)
    class Meta:
        model = Customer
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'reviews',
            'carts',
            'orders',
        )
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user= Customer(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ReviewSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only = True)
    product = ProductSerializer(read_only = True)
    class Meta:
        model =Review
        fields = '__all__'



class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    farmer_name = serializers.CharField(source='farmer.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'product_name', 'farmer', 'farmer_name']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'status', 'created_at', 'updated_at', 'items']


class OrderSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only = True)
    cart = CartSerializer(read_only = True)
    items = OrderItemSimpleSerializer(many = True, read_only = True)
    
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only = True)
    product = ProductSerializer(read_only = True)
    discount = DiscountSimpleSerializer(read_only= True)
    class Meta:
        model = OrderItem
        fields = '__all__'