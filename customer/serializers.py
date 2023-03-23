from rest_framework import serializers
from customer.models import *
import re
from django.contrib.auth.hashers import make_password

class AddressSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        address = Address(
            type = validated_data['type'],
            house_no = validated_data['house_no'],
            street_no = validated_data['street_no'],
            locality = validated_data['locality'],
            city = validated_data['city'],
            state = validated_data['state'],
            country = validated_data['country'],
            pincode = validated_data['pincode']
        )

        address.save()
        return address
    
    def update(self, address, validated_data):
        address.type = validated_data.get('type', address.type)
        address.house_no = validated_data.get('house_no', address.house_no)
        address.street_no = validated_data.get('street_no', address.street_no)
        address.locality = validated_data.get('locality', address.locality)
        address.city = validated_data.get('city', address.city)
        address.state = validated_data.get('state', address.state)
        address.country = validated_data.get('country', address.country)
        address.pincode = validated_data.get('pincode', address.pincode)

        address.save()
        return address

    class Meta:
        model = Address
        fields = ['type','house_no', 'street_no', 'locality', 'city', 'state', 'country', 'pincode']


class CustomUserSerializer(serializers.ModelSerializer):
    def validate_password(self, password):
        if len(password)<8:
            raise serializers.ValidationError("Password must be 8 characters long.")
        
        if not re.search('[a-z]', password):
            raise serializers.ValidationError("Password must contain at least one lowercase character.")
        
        if not re.search('[A-Z]', password):
            raise serializers.ValidationError("Password must contain at least one uppercase character.")
        
        if not re.search('[0-9]', password):
            raise serializers.ValidationError("Password must contain at least one numeric character.")    
        
        if not re.search('[!@#$%&]', password):
            raise serializers.ValidationError("Password must contain at least one of these special character - [!@#$%&].")
        
        return password

    def create(self, validate_data):
        # address_data = validate_data.pop('address')
        user = CustomUser(
            email = validate_data['email'],
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name'],
            mobile_no = validate_data['mobile_no']
        )
        raw_password = validate_data['password']
        user.password = make_password(raw_password)         #Encrypting raw_password
        
        user.save()

        # address = AddressSerializer.create(self, validated_data=address_data)
        # user.address.add(address)
        
        # user.save()
        return user
    
    def update(self, user, validated_data):
        user.email = validated_data.get('email', user.email)
        if validated_data.get('password', None) == None:
            pass
        else:
            user.password = make_password(validated_data['password'])

        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.mobile_no = validated_data.get('mobile_no', user.mobile_no)
        
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = '__all__'
