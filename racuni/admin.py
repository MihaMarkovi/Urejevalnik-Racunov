from django.contrib import admin
from .models import Company, Bill, Product

# Register your models here.
admin.site.register(Company)
admin.site.register(Bill)
admin.site.register(Product)