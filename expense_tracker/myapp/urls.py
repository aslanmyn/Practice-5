from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('accounts/', include('allauth.urls')),
    path('categories/', views.category_list, name='category_list'),
    path('add_category/', views.add_category, name='category_add'),
    path('group_expenses/', views.group_expense_list, name='group_expense_list'),
    path('group_expenses/add/', views.add_group_expense, name='add_group_expense'),
    path('expenses/', views.expense_list, name='expenses'),
    
]

