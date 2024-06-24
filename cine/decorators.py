from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.conf import settings
import jwt

def my_custom_middleware(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Custom middleware logic
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Additional logic to check user_id or other conditions
        # For example, you might check if the user_id exists in the database or if the user is authenticated

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def jwt_token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Extract the token from the request header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'error': 'Token is missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        print("----------- " + token + " ----------")
        
        try:
            # Decode the token
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded.get('user_id')

            # Set the user_id in the request for further use
            request.user_id = user_id
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Token is valid, proceed to the view
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view