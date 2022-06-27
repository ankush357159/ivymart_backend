# Django Import
from django.contrib.auth.models import User

# Rest Framework Import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

# Local Import
from ivymart.serializers.jwtSerializers import UserSerializer


# Create New User
class RegisterUserCreatView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer


# Get User Details / User Profile
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# Update User / User Profile update
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    data = request.data
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.username = data["username"]
    user.email = data["email"]
    
    user.save()
    return Response(serializer.data)


# List of Users -- Admin
@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Details of a User -- Admin
@api_view(["GET"])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    users = User.objects.get(id=pk)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

# Update a User -- Admin
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.username = data["username"]    
    user.email = data["email"]
    # user.is_staff = data["isAdmin"]

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# Delete User -- Admin
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response("User was deleted")
