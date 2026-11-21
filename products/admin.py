from django.contrib import admin

from .models import Category, Product

admin.site.site_header = 'Campus Supply administration'
admin.site.site_title = 'Campus Supply admin'
admin.site.index_title = 'Catalog and account management'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_by', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    list_select_related = ('category', 'created_by')
    autocomplete_fields = ('category',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
