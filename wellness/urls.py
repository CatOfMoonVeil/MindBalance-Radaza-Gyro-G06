from django.urls import path
from . import views

app_name = 'wellness'

urlpatterns = [
    path('', views.log_list, name='log_list'),
    path('new/', views.log_create, name='log_create'),
    path('<int:pk>/edit/', views.log_update, name='log_update'),
    path('<int:pk>/delete/', views.log_delete, name='log_delete'),
    path('trends/', views.weekly_trends, name='weekly_trends'),
    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),
]