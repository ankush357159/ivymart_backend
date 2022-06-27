from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=50)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    email = serializers.EmailField(
        max_length=255,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(max_length=50)
    is_active = serializers.BooleanField(default=True)
    is_staff = serializers.BooleanField(default=False)


    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name", "is_active", "is_staff"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user







