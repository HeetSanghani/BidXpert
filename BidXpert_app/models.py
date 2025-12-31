from django.db import models
from datetime import date, time
from django.contrib.auth.models import AbstractUser


# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)  # Use EmailField for emails
    contact_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    address = models.TextField()
    aadhar_number = models.CharField(max_length=12, unique=True)  # Ensuring Aadhar is unique

    def __str__(self):
        return self.username



class Categories(models.Model):
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.category




# Main Product Model
from django.db import models
from datetime import date, time


class Product(models.Model):
    product = models.CharField(max_length=255)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    other_information = models.TextField(blank=True, null=True)

    # Date & Time (Defaults to now if not provided)
    date = models.DateField(default=date.today, blank=True, null=True)
    time = models.TimeField(default=time, blank=True, null=True)
    end_date = models.DateTimeField(null=True,blank=True)
    # Financial Fields
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # New field to track current highest bid
    current_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Extra Fields as JSON (For flexible additional info)
    extra_fields = models.JSONField(default=dict, blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    winner = models.ForeignKey('Bid',on_delete=models.CASCADE,related_name='product_winnerbid',null=True,blank=True)
    
    def __str__(self):
        return self.product


# Product Image Model (Supports Multiple Images per Product)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds timestamp

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.product.product}"