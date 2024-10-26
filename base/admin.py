from django.contrib import admin

# Register your models here.
from .models import Product , Book, BookCategory


admin.site.register(Product)
admin.site.register(Book)
admin.site.register(BookCategory)
