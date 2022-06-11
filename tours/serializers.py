from django.db.models import Avg

from rest_framework import serializers

from .models import Tour, Comment


class TourSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('rating'))

    class Meta:
        model = Tour
        fields = [
            'id',
            'name',
            'description',
            'price',
            'company',
            'start_date',
            'end_date',
            'average_rating'
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'user',
            'created_at'
        ]


class TourDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True)

    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('rating'))

    class Meta:
        model = Tour
        fields = [
            'id',
            'name',
            'description',
            'price',
            'company',
            'start_date',
            'end_date',
            'average_rating',
            'comments'
        ]