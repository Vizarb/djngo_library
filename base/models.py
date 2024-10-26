from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the id field
    desc = models.CharField(max_length=50,null=True,blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    createdTime=models.DateTimeField(auto_now_add=True)
    fields =['desc','price']
 
    def __str__(self):
           return self.desc
    
    from django.db import models

class BookCategory(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the id field
    name = models.CharField(max_length=50, unique=True, null=False)  # Name of the category

    def __str__(self):
        return self.name  # Return the category name


class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly define the id field
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='books')  # Link to BookCategory

    def __str__(self):
        return f"{self.title} by {self.author}"