from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import  viewsets, permissions, status
from .serializers import CustomerSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Farmer, Product, Review, Discount, Cart, CartItem, Order, OrderItem
from django.contrib.auth import authenticate


'''
registration of new user in the customer serializer the create is called and the password is hashed and in the serializer itself
the creation of the new user happens
'''
class AuthenticationViewSet (viewsets.ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
            if self.action in ['list', 'retrieve']:
                return [permissions.IsAdminUser()]
            return [permissions.AllowAny()]
    
    @action(detail= False, methods=['post'])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": CustomerSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status= status.HTTP_201_CREATED)
    
    ''' login '''
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username= username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                 "message": "logged in successfully",
                 "refresh": str(refresh),
                 "access": str(refresh.access_token),
                 }, status= status.HTTP_201_CREATED)
        else:
             return Response ({
                  "detail": "Invalid Credentials"}, status= status.HTTP_401_UNAUTHORIZED)
