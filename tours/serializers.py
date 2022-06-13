from django.db.models import Avg

from rest_framework import serializers

from .models import Tour, Comment, TourImage, Rating, Saved


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


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class TourImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourImage
        fields = "__all__"


class TourDetailSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)
    images = TourImageSerializer(many=True)
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
            'images',
            'comments'
        ]


class SavedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tour = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Saved
        fields = "__all__"


# class SavedSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True)
    
#     class Meta:
#         model = Saved
#         fields = "__all__"