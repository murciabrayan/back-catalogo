from django.contrib import admin

from .models import AdditionalOption, Product, ProductColorOption


class ProductColorOptionInline(admin.TabularInline):
    model = ProductColorOption
    extra = 1


@admin.register(AdditionalOption)
class AdditionalOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'display_order')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'accent', 'is_active', 'display_order')
    list_filter = ('category', 'accent', 'is_active')
    search_fields = ('name', 'description', 'includes')
    ordering = ('display_order', 'name')
    filter_horizontal = ('additional_options',)
    inlines = [ProductColorOptionInline]


@admin.register(ProductColorOption)
class ProductColorOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'display_order')
    search_fields = ('name', 'product__name')
    ordering = ('product__name', 'display_order')
