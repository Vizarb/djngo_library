from rest_framework import serializers
from .models import Product , Book , BookCategory




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookCatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'
