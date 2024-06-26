from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from .models import User
from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .utils import generate_access_token
from django.contrib.auth import authenticate

from .decorators import jwt_token_required

# Create your views here.
@api_view(['GET'])
def home(request):
    return HttpResponse("Hello World from Python Dejango, Welcome Home.")


@api_view(['POST'])
def register(request):
    nickname = request.data.get('nickname')
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password or not nickname:
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        request.data['password'] = make_password(password)  # Hash the password before serialization
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):

    email = request.data.get('email')
    password = request.data.get('password')
    user = get_object_or_404(User, email=request.data['email'])
    print("---------")
    if not check_password(password, user.password):
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
    print("/////////")
    user_token = generate_access_token(user)    
    serializer = UserSerializer(instance=user)
    print("/////////")
    return Response({"token":user_token,"user": serializer.data})
    
@api_view(['GET'])
@jwt_token_required
def get_all_users(request):
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['Get'])
@jwt_token_required
def get_user_by_id(request):
    try:
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)