from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer

from .models import Cart, CartItem, Order, OrderItem, Product, Review
from .serializers import OrderSerializer, ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    @action(detail= False, methods = ['get'])
    def reviews( self, request, product_id=None):
        if product_id:
            reviews = Review.objects.filter(product_id = product_id)
            if not reviews.exists(): 
                return Response( {"error": "No reviews found for this product"}, status= status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        reviews = Review.objects.filter(user = self.request.user)
        if not reviews.exists():
            return Response(
                {"error": "You have not written any reviews"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        if product_id :
            try:
               product = Product.objects.filter(pk=product_id)
            except Product.DoesNotExist :
               return Response({"error":"the product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if Review.objects.filter(user = self.request.user, product= product).exists():
           return Response({"error":"the review for this already exists"})
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)