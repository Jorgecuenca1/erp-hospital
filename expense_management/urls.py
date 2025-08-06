from django.urls import path
from . import views

app_name = 'expense_management'

urlpatterns = [
    path('', views.expense_dashboard, name='dashboard'),
    path('reports/', views.expense_reports, name='reports'),
    path('categories/', views.expense_categories, name='categories'),
    path('policies/', views.expense_policies, name='policies'),
] 