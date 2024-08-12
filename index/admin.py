from django.contrib import admin
from .models import Category, Product, Cart


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'id']
    # list_filter = ['created_at']
    list_display = ['id', 'name']
    ordering = ['-id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['pr_name', 'id']
    list_display = ['pr_name', 'id']
    ordering = ['-id']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ['user_product', 'id']
    list_display = ['user_product', 'id']
    ordering = ['-id']
