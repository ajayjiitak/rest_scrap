from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate  # Import authenticate function



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','date_joined')

class RegisterSerializer(serializers.ModelSerializer):
    # Added password confirmation field
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate_username(self, value):
        # Validate uniqueness of username
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def validate_email(self, value):
        # Validate uniqueness of email
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate(self, data):
        # Validate that passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password confirmation before creating user
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user



# class LoginSerializer(serializers.Serializer):
#     username=serializers.CharField(required=True)
#     password=serializers.CharField(required=True, write_only=True)


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True, write_only=True)

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         if username and password:
#             user = authenticate(username=username, password=password)
#             if user is None:
#                 raise serializers.ValidationError('Invalid credentials')
#         else:
#             raise serializers.ValidationError('Both fields are required')

#         return attrs

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Both fields are required')

        return attrs
    


class SimpleProductSerializer(serializers.Serializer):
    product_title = serializers.CharField()
    price = serializers.FloatField()
    photos = serializers.ListField(child=serializers.URLField())
    product_url = serializers.URLField()

class DetailedProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    brand = serializers.CharField()
    category = serializers.CharField()
    photos = serializers.ListField(child=serializers.URLField())
    condition = serializers.CharField()
    seller = serializers.CharField()