from rest_framework import serializers
from feature.models import *

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
    # def create(self, validated_data):
    #     pass

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = '__all__'
