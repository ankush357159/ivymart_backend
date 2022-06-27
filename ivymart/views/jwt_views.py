from rest_framework_simplejwt.views import TokenObtainPairView
from ivymart.serializers.jwtSerializers import MyTokenObtainPairSerializer

# Rest Framework Import
from rest_framework.permissions import AllowAny

# Local Import 

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny,]
    serializer_class = MyTokenObtainPairSerializer
    