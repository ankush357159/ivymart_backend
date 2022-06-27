# Rest Framework JWT 
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Django
from django.contrib.auth.models import User

# Local import
from ivymart.serializers.userSerializers import UserSerializer


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

        def get_token(self, obj):
            token = RefreshToken.for_user(obj)
            return str(token.access_token)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
       
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['message'] = "Welcome to IvyMart"
        

        return token