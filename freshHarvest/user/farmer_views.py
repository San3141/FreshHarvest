from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from .models import Farmer
from .serializers import FarmerSerializer

class FarmerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated]


