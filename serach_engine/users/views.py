from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser 
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = CustomUser .objects.all()
    serializer_class = UserSerializer
    
# Login User (Menggunakan email & password)
class UserLogin(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password) 

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            first_name = user.full_name.split()[0] 
            
            return Response(
                {
                    'message': f'Login berhasil! Selamat datang, {first_name}!',
                    'token': token.key
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {'error': 'Email atau password salah. Silakan coba lagi.'},
            status=status.HTTP_400_BAD_REQUEST
        )
