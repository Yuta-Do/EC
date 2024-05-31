from django.contrib import admin
from .models import Category, Product

# Register your models here.
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category,ObjectAdmin)
admin.site.register(Product,ObjectAdmin)