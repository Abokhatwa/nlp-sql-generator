from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(username=email, password=password)
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data,
                'accessible_databases': user.get_accessible_databases()
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid credentials or account is inactive'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'success': True, 'message': 'Logged out successfully'})
    except TokenError:
        # Token is already blacklisted or invalid
        return Response({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'user': UserSerializer(user).data,
        'accessible_databases': user.get_accessible_databases(),
        'role': user.role.name if user.role else None
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_session(request):
    """Validate if the current session/token is still valid"""
    try:
        # Token is already validated by IsAuthenticated permission
        # Additional checks can be added here
        user = request.user
        if not user.is_active:
            return Response({
                'valid': False,
                'message': 'User account is inactive'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'valid': True,
            'user': user.username
        })
    except Exception as e:
        return Response({
            'valid': False,
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)

@never_cache
def login_page(request):
    # Clear any existing session data
    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@never_cache
def dashboard_page(request):
    response = render(request, 'dashboard.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response