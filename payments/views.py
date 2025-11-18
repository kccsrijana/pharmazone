from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone
from .models import Payment, Refund, Coupon, CouponUsage
from .forms import CouponForm
from orders.models import Order
import json
import uuid


@login_required
def process_payment(request, order_id):
    """Process payment for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status == 'paid':
        messages.info(request, 'This order has already been paid.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Create payment record
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'user': request.user,
            'amount': order.total_amount,
            'payment_method': order.payment_method,
            'status': 'pending'
        }
    )
    
    context = {
        'order': order,
        'payment': payment,
        'payment_method': order.payment_method,
    }
    return render(request, 'payments/process_payment.html', context)


@login_required
@require_POST
def confirm_payment(request, payment_id):
    """Confirm payment (simulated)"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    # Simulate payment processing
    payment.status = 'completed'
    payment.completed_at = timezone.now()
    payment.gateway_transaction_id = f"TXN_{uuid.uuid4().hex[:12].upper()}"
    payment.save()
    
    # Update order payment status
    payment.order.payment_status = 'paid'
    payment.order.status = 'confirmed'
    payment.order.confirmed_at = timezone.now()
    payment.order.save()
    
    # Create order status history
    from orders.models import OrderStatusHistory
    OrderStatusHistory.objects.create(
        order=payment.order,
        status='confirmed',
        notes='Payment completed successfully',
        changed_by=request.user
    )
    
    messages.success(request, 'Payment completed successfully!')
    return redirect('orders:order_detail', order_id=payment.order.id)


@login_required
def payment_success(request, payment_id):
    """Payment success page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
        'order': payment.order,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_failed(request, payment_id):
    """Payment failed page"""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    context = {
        'payment': payment,
        'order': payment.order,
    }
    return render(request, 'payments/payment_failed.html', context)


@login_required
def apply_coupon(request):
    """Apply coupon code"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        order_id = request.POST.get('order_id')
        
        if coupon_code and order_id:
            try:
                order = Order.objects.get(id=order_id, user=request.user)
                coupon = Coupon.objects.get(code=coupon_code)
                
                # Check if coupon is valid
                if not coupon.is_valid:
                    return JsonResponse({'success': False, 'message': 'Coupon has expired or is inactive.'})
                
                # Check if user can use this coupon
                if not coupon.can_be_used_by_user(request.user):
                    return JsonResponse({'success': False, 'message': 'You have already used this coupon.'})
                
                # Check minimum order amount
                if order.subtotal < coupon.minimum_order_amount:
                    return JsonResponse({
                        'success': False, 
                        'message': f'Minimum order amount is ₹{coupon.minimum_order_amount}'
                    })
                
                # Calculate discount
                if coupon.coupon_type == 'percentage':
                    discount_amount = (order.subtotal * coupon.value) / 100
                    if coupon.maximum_discount:
                        discount_amount = min(discount_amount, coupon.maximum_discount)
                else:  # fixed amount
                    discount_amount = coupon.value
                
                # Apply discount
                order.discount_amount = discount_amount
                order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost - discount_amount
                order.save()
                
                # Record coupon usage
                CouponUsage.objects.create(
                    coupon=coupon,
                    user=request.user,
                    order=order,
                    discount_amount=discount_amount
                )
                
                return JsonResponse({
                    'success': True,
                    'message': f'Coupon applied successfully! You saved ₹{discount_amount}',
                    'discount_amount': float(discount_amount),
                    'new_total': float(order.total_amount)
                })
                
            except Coupon.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
            except Order.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Order not found.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


@login_required
def remove_coupon(request, order_id):
    """Remove applied coupon"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Remove coupon usage
    CouponUsage.objects.filter(order=order).delete()
    
    # Recalculate total
    order.discount_amount = 0
    order.total_amount = order.subtotal + order.tax_amount + order.shipping_cost
    order.save()
    
    messages.success(request, 'Coupon removed successfully.')
    return redirect('orders:checkout')


@login_required
def refund_request(request, order_id):
    """Request refund for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status != 'paid':
        messages.error(request, 'Only paid orders can be refunded.')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Get or create payment record for the order
    try:
        payment = Payment.objects.get(order=order)
    except Payment.DoesNotExist:
        # Create payment record if it doesn't exist
        payment = Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total_amount,
            payment_method=order.payment_method,
            status='completed'
        )
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            # Create refund request
            refund = Refund.objects.create(
                payment=payment,
                amount=order.total_amount,
                reason=reason,
                status='pending'
            )
            
            messages.success(request, 'Refund request submitted successfully.')
            return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
    }
    return render(request, 'payments/refund_request.html', context)


@login_required
def payment_history(request):
    """View payment history"""
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_history.html', context)


# Admin views for payment management
@login_required
def admin_payment_list(request):
    """Admin view for all payments"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    payments = Payment.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    context = {
        'payments': payments,
        'status_choices': Payment.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'payments/admin_payment_list.html', context)


@login_required
def admin_refund_list(request):
    """Admin view for refund requests"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    refunds = Refund.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        refunds = refunds.filter(status=status_filter)
    
    context = {
        'refunds': refunds,
        'status_choices': Refund.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'payments/admin_refund_list.html', context)


@login_required
def process_refund(request, refund_id):
    """Process refund request (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    refund = get_object_or_404(Refund, id=refund_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'approve':
            refund.status = 'completed'
            refund.processed_by = request.user
            refund.admin_notes = admin_notes
            refund.completed_at = timezone.now()
            refund.save()
            
            # Update payment refund amount
            refund.payment.refund_amount = refund.amount
            refund.payment.save()
            
            messages.success(request, 'Refund approved and processed.')
        elif action == 'reject':
            refund.status = 'failed'
            refund.processed_by = request.user
            refund.admin_notes = admin_notes
            refund.save()
            
            messages.success(request, 'Refund request rejected.')
        
        return redirect('payments:admin_refund_list')
    
    context = {
        'refund': refund,
    }
    return render(request, 'payments/process_refund.html', context)


@login_required
def coupon_management(request):
    """Coupon management (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    coupons = Coupon.objects.all().order_by('-created_at')
    
    context = {
        'coupons': coupons,
    }
    return render(request, 'payments/coupon_management.html', context)