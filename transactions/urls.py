from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),
    path('data/', views.transaction_data, name='transaction_data'),
    path('comparison-data/', views.comparison_data, name='comparison_data'),
    path('comparison-chart/', views.comparison_chart, name='comparison_chart'),
    path('summary/', views.transaction_summary, name='transaction_summary'),
]
