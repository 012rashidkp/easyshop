from rest_framework import serializers
from .models import Products,CartItem,Cart
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import exceptions

from django.contrib.auth import get_user_model

User=get_user_model()
 #from django.contrib.auth.models import User




class ProductSerializer(serializers.ModelSerializer):
    #prod_id = serializers.IntegerField(source='id')
    #id = serializers.CharField()
    prod_id = serializers.CharField(source='id')
    class Meta:
            model =Products
            fields = ['prod_id', 'pname','pstock','pdesc','prod_price','document']
            
           
# user registration Api

class UserSerializer(serializers.ModelSerializer):
    #userid = serializers.CharField(source='id',read_only=True)
    password=serializers.CharField(max_length=65,min_length=6,write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password'
        ]

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email is already in use')})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



#  user login Api    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                
                err={
                    'error': True,
                    'message':"Unable to login with given credentials."
                }
                #return Response(err)
               # msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(err)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data
