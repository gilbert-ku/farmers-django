from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Agrovet, Farmer
from .serializers import (
    AgrovetRegistrationSerializer, FarmerRegistrationSerializer,
    LoginSerializer, PasswordResetSerializer, AgrovetSerializer,
    FarmerSerializer, UserSerializer
)

class AgrovetRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AgrovetRegistrationSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': user.user_type,
                'must_reset_password': user.must_reset_password,
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_reset_view(request):
    if not request.user.must_reset_password:
        return Response({'error': 'Password reset not required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(request.user)
        return Response({'message': 'Password reset successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agrovet_dashboard_view(request):
    if request.user.user_type != 'agrovet':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    agrovet = request.user.agrovet_profile
    farmers = Farmer.objects.filter(registered_by=agrovet)
    
    return Response({
        'agrovet': AgrovetSerializer(agrovet).data,
        'farmers': FarmerSerializer(farmers, many=True).data,
        'total_farmers': farmers.count()
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_farmer_view(request):
    if request.user.user_type != 'agrovet':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = FarmerRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        farmer = serializer.save()
        return Response({
            'message': 'Farmer registered successfully',
            'farmer': FarmerSerializer(farmer).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def farmer_dashboard_view(request):
    if request.user.user_type != 'farmer':
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user.must_reset_password:
        return Response({
            'error': 'Password reset required',
            'must_reset_password': True
        }, status=status.HTTP_400_BAD_REQUEST)
    
    farmer = request.user.farmer_profile
    return Response({
        'farmer': FarmerSerializer(farmer).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    return Response({
        'user': UserSerializer(request.user).data
    })
