
from django.contrib import admin
from BidXpert_app import models
from .models import ContactMessage


# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(models.Categories)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.CustomUser)
admin.site.register(models.Bid)

