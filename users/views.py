from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from django_ratelimit.decorators import ratelimit
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

from .serializers import CustomTokenObtainPairSerializer, RegistrationSerializer 
from .permissions import IsAdmin


import logging
logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
    request_body=RegistrationSerializer,
    responses={
        201: "User registered successfully",
        400: "Invalid data",
    }
)
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Validate password strength
                validate_password(request.data['password1'])
            except ValidationError as e:
                return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            logger.info(f"New user registered: {user.username}")
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"Failed registration attempt: {serializer.errors}")
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Login endpoint that returns JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'role': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Invalid credentials",
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        logger.info(f"Login attempt by user: {request.data.get('username')}")
        return response 
    
@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):
    return Response({"message": "Welcome to the admin dashboard"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({"message": f"Welcome, {request.user.username}"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.user.role == 'admin':
        return Response({"message": "Admin dashboard"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User dashboard"}, status=status.HTTP_200_OK)
