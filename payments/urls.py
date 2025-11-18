from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment URLs
    path('process/<int:order_id>/', views.process_payment, name='process_payment'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('failed/<int:payment_id>/', views.payment_failed, name='payment_failed'),
    path('history/', views.payment_history, name='payment_history'),
    
    # Coupon URLs
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/<int:order_id>/', views.remove_coupon, name='remove_coupon'),
    
    # Refund URLs
    path('refund/<int:order_id>/', views.refund_request, name='refund_request'),
    
    # Admin URLs
    path('admin/', views.admin_payment_list, name='admin_payment_list'),
    path('admin/refunds/', views.admin_refund_list, name='admin_refund_list'),
    path('admin/refunds/<int:refund_id>/', views.process_refund, name='process_refund'),
    path('admin/coupons/', views.coupon_management, name='coupon_management'),
]
