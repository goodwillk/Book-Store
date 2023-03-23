from rest_framework import serializers
from product.models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
    # def create(user, validated_data):
    #     review = Review(
    #         custom_user_id = user,
    #         rating = validated_data['rating'],
    #         description = validated_data['description']
    #     )
        
    #     review.save()
    #     return review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
