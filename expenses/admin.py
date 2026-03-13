from django.contrib import admin
from .models import Category, Department, Expense


admin.site.register(Category)
admin.site.register(Department)
admin.site.register(Expense)