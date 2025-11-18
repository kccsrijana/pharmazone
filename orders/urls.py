from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Customer URLs
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('<int:order_id>/prescription/', views.prescription_upload, name='prescription_upload'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('addresses/', views.shipping_addresses, name='shipping_addresses'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('addresses/<int:address_id>/default/', views.set_default_address, name='set_default_address'),
    
    # Admin URLs
    path('admin/', views.admin_order_list, name='admin_order_list'),
    path('admin/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('prescription/<int:prescription_id>/review/', views.prescription_review, name='prescription_review'),
]
