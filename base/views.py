# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status

from base.utils_copy import track_failed_login_attempts
from .models import Product, Book, BookCategory
from .serializer import ProductSerializer, BookSerializer, BookCatagorySerializer
from base.utils import log_function_call

@api_view(['GET'])
def index(req):
    return JsonResponse('hello', safe=False)

@api_view(['GET'])
def Librery(req):
    all_books = BookSerializer(Book.objects.all(), many=True).data
    return JsonResponse(all_books, safe=False)

@api_view(['GET'])
def Products(req):
    all_products = ProductSerializer(Product.objects.all(), many=True).data
    return JsonResponse(all_products, safe=False)

@api_view(['GET'])
def BookCategorys(req):
    all_book_catagorey = BookCatagorySerializer(BookCategory.objects.all(), many=True).data
    return JsonResponse(all_book_catagorey, safe=False)

@track_failed_login_attempts
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful', 'is_staff': user.is_staff})
    else:
        return JsonResponse({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@log_function_call
@api_view(['POST'])
def register_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    try:
        user = User.objects.create_user(username=username, password=make_password(password), email=email)
        return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@log_function_call
@login_required
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@log_function_call
@api_view(['GET'])
def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True, 'username': request.user.username}, status=status.HTTP_200_OK)
    return JsonResponse({'is_authenticated': False}, status=status.HTTP_200_OK)
