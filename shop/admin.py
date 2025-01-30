from django.contrib import admin
from .models import Type, Product, ProductReview

# Register your models here.
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Type, TypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'type', 'stock','available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    list_per_page = 20

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)