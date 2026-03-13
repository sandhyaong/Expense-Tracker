from django.urls import path
from . import views

urlpatterns = [

path('', views.dashboard),
path('add-expense/', views.add_expense),
path('expenses/', views.expense_list),
path('export/', views.export_csv),
path('approve/<int:id>/', views.approve_expense, name="approve_expense"),
path('reject/<int:id>/', views.reject_expense, name="reject_expense"),
path("categories/", views.category_list, name="categories"),
path("approvals/", views.approvals, name="approvals"),
path("add-category/", views.add_category),
# department
path("departments/", views.department_list),
path("departments/add/", views.add_department, name="add_department"),
path("departments/edit/<int:id>/", views.edit_department, name="edit_department"),
path("departments/delete/<int:id>/", views.delete_department, name="delete_department"),
]