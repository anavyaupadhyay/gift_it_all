from django.shortcuts import render
from custom_users.serializers import CustomAuthTokenSerializer, CustomUserCreateSerializer

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class CustomUserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        # You can also return the token in the response if needed

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Customize the response format
        response_data = {
            'token': token.key,
            'email': user.email,  # Include the user's email
        }

        return Response(response_data, status=status.HTTP_200_OK)
