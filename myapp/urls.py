from django.urls import path
from . import views

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
   #delete order
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
    
]