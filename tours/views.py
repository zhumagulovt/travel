from rest_framework import generics

from .models import Tour
from .serializers import TourSerializer, TourDetailSerializer


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer


class TourDetail(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer
