# urls.py
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('products/', views.Products, name='products'),  # Products page
    path('library/', views.Librery, name='library'),  # Library page
    path('bookcategories/', views.BookCategorys, name='book_categories'),  # Book categories page
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Registration page
    path('logout/', views.logout_view, name='logout'),  # Logout page

    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
]
