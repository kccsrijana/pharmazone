from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment URLs
    path('process/<int:order_id>/', views.process_payment, name='process_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('failed/<int:payment_id>/', views.payment_failed, name='payment_failed'),
    path('history/', views.payment_history, name='payment_history'),
    path('verify-esewa/', views.verify_esewa_payment, name='verify_esewa_payment'),
    
    # eSewa Simulator URLs (Development-friendly)
    path('esewa-simulator/', views.esewa_simulator, name='esewa_simulator'),
    path('esewa-simulator-success/<int:payment_id>/', views.esewa_simulator_success, name='esewa_simulator_success'),
    path('esewa-simulator-failure/<int:payment_id>/', views.esewa_simulator_failure, name='esewa_simulator_failure'),
    
    # eSewa callback URLs (Real eSewa Test API)
    path('esewa-success/<int:payment_id>/', views.esewa_success, name='esewa_success'),
    path('esewa-failure/<int:payment_id>/', views.esewa_failure, name='esewa_failure'),
    
    # Coupon URLs
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/<int:order_id>/', views.remove_coupon, name='remove_coupon'),
    
    # Refund URLs
    path('refund/<int:order_id>/', views.refund_request, name='refund_request'),
    
    # Invoice URLs
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/download/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('invoice/<int:invoice_id>/view/', views.view_invoice_pdf, name='view_invoice_pdf'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    
    # Admin URLs
    path('admin/', views.admin_payment_list, name='admin_payment_list'),
    path('admin/refunds/', views.admin_refund_list, name='admin_refund_list'),
    path('admin/refunds/<int:refund_id>/', views.process_refund, name='process_refund'),
    path('admin/coupons/', views.coupon_management, name='coupon_management'),
    path('admin/order/<int:order_id>/create-invoice/', views.create_invoice_for_order_view, name='create_invoice_for_order'),
]
