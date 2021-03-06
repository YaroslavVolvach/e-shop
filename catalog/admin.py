from django.contrib import admin
from .models import Product, Category, Gallery


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Category, CategoryAdmin)


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'category', 'description', 'price',
                    'quantity')
    inlines = [GalleryInline, ]


admin.site.register(Product, ProductAdmin)
