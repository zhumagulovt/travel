from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from django_filters import rest_framework as filters

from .models import Tour, Comment, Rating, Saved, UserTourViewed
from .serializers import TourSerializer, TourDetailSerializer, \
    CommentSerializer, RatingSerializer, RatingUpdateSerializer, SavedSerializer
from .permissions import IsOwnerOrReadOnly


class TourFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    start = filters.DateFilter(field_name="start_date", lookup_expr='gte')
    end = filters.DateFilter(field_name="end_date", lookup_expr='lte')

    class Meta:
        model = Tour
        fields = ['min_price', 'max_price']


class TourListView(generics.ListAPIView):
    queryset = Tour.objects.all()
    filterset_class = TourFilter
    serializer_class = TourSerializer


class TourDetail(generics.RetrieveAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourDetailSerializer

    def get_object(self):
        obj = super().get_object()
        self.user_viewed(obj, now())
        return obj
    
    def user_viewed(self, obj, timestamp):
        user = self.request.user
        if not user.is_authenticated:
            return
        tour_view, _ = UserTourViewed.objects.get_or_create(user=user, tour=obj)
        tour_view.timestamp = timestamp
        tour_view.save()
        return tour_view


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RatingViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_object(self):
        return get_object_or_404(
            Rating, 
            tour_id=self.kwargs['pk'],
            user=self.request.user
            )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == "update":
            return RatingUpdateSerializer
        return super().get_serializer_class()


class SavedView(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    queryset = Saved.objects.all()
    serializer_class = SavedSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_object(self):
        return get_object_or_404(
            Saved, 
            tour_id=self.kwargs['pk'], 
            user=self.request.user
        )
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(
            tour_id=self.kwargs['pk'],
            user=self.request.user
            )

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
