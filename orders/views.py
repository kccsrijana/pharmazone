from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem, OrderStatusHistory, ShippingAddress
from .forms import CheckoutForm, ShippingAddressForm
from cart.models import Cart, CartItem
from products.models import Medicine, Prescription
from payments.models import Payment
import uuid


@login_required
def order_list(request):
    """View user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


def is_secure_admin(user):
    """Check if user is a secure admin"""
    return (user.is_authenticated and 
            user.is_staff and 
            user.username == 'admin')


@login_required
def checkout(request):
    """Checkout process"""
    # Prevent admin users from accessing checkout
    if is_secure_admin(request.user):
        messages.error(request, 'Admin users cannot place orders.')
        return redirect('doctor_appointments:admin_dashboard')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart')
    
    # Check if any medicines require prescription
    requires_prescription = any(
        item.medicine.requires_prescription for item in cart_items
    )
    
    # Get user's saved addresses
    saved_addresses = ShippingAddress.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        
        # Display form errors if any
        if not form.is_valid():
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.requires_prescription = requires_prescription
                    
                    # Get payment method
                    payment_method = request.POST.get('payment_method', 'cod')
                    order.payment_method = payment_method
                    
                    # Set default values for optional fields
                    if not order.shipping_state:
                        order.shipping_state = ''
                    if not order.shipping_postal_code:
                        order.shipping_postal_code = ''
                    
                    # Calculate totals
                    from decimal import Decimal
                    subtotal = sum(item.total_price for item in cart_items)
                    tax_amount = Decimal('0.00')  # No tax
                    shipping_cost = Decimal('100.00') if subtotal < 2000 else Decimal('0.00')  # Free shipping above Rs. 2000
                    total_amount = subtotal + shipping_cost
                    
                    order.subtotal = subtotal
                    order.tax_amount = tax_amount
                    order.shipping_cost = shipping_cost
                    order.total_amount = total_amount
                    order.save()
                    
                    # Handle prescription upload if required
                    if requires_prescription:
                        prescription_image = request.FILES.get('prescription_image')
                        doctor_name = request.POST.get('doctor_name')
                        doctor_license = request.POST.get('doctor_license', '')
                        prescription_date = request.POST.get('prescription_date')
                        prescription_notes = request.POST.get('prescription_notes', '')
                        
                        if prescription_image and doctor_name and prescription_date:
                            # Get the first medicine that requires prescription
                            prescription_medicine = None
                            for item in cart_items:
                                if item.medicine.requires_prescription:
                                    prescription_medicine = item.medicine
                                    break
                            
                            if prescription_medicine:
                                # Create prescription record
                                prescription = Prescription.objects.create(
                                    user=request.user,
                                    medicine=prescription_medicine,
                                    prescription_image=prescription_image,
                                    doctor_name=doctor_name,
                                    doctor_license=doctor_license,
                                    prescription_date=prescription_date,
                                    notes=prescription_notes,
                                    status='pending'
                                )
                                
                                # Link prescription to order
                                order.prescription = prescription
                                order.save()
                        else:
                            messages.error(request, 'Please upload prescription with all required details.')
                            order.delete()
                            return redirect('orders:checkout')
                    
                    # Create order items
                    for cart_item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            medicine=cart_item.medicine,
                            quantity=cart_item.quantity,
                            unit_price=cart_item.medicine.current_price,
                            medicine_name=cart_item.medicine.name,
                            medicine_strength=cart_item.medicine.strength,
                            medicine_dosage_form=cart_item.medicine.dosage_form,
                        )
                        
                        # Update stock
                        cart_item.medicine.stock_quantity -= cart_item.quantity
                        cart_item.medicine.save()
                    
                    # Create order status history
                    OrderStatusHistory.objects.create(
                        order=order,
                        status='pending',
                        notes='Order created successfully'
                    )
                    
                    # Clear cart
                    cart.items.all().delete()
                    
                    # Send notifications
                    from notifications.services import NotificationService
                    NotificationService.notify_new_order(order)
                    
                    # Check if it's a prescription order
                    if requires_prescription:
                        NotificationService.notify_prescription_order(order)
                    
                    # Handle payment based on method
                    if payment_method == 'cod':
                        # Cash on Delivery - order is placed, payment pending
                        messages.success(request, 'Order placed successfully! Pay when you receive your order.')
                        return redirect('orders:order_detail', order_id=order.id)
                    elif payment_method == 'esewa':
                        # Online payment - redirect to payment gateway
                        messages.success(request, 'Order created! Redirecting to payment...')
                        return redirect('payments:process_payment', order_id=order.id)
                    else:
                        messages.success(request, 'Order placed successfully!')
                        return redirect('orders:order_detail', order_id=order.id)
                    
            except Exception as e:
                messages.error(request, f'Error creating order: {str(e)}')
    else:
        form = CheckoutForm()
        address_form = ShippingAddressForm()
    
    # Calculate totals for display
    from decimal import Decimal
    subtotal = sum(item.total_price for item in cart_items)
    tax_amount = Decimal('0.00')  # No tax
    shipping_cost = Decimal('100.00') if subtotal < 2000 else Decimal('0.00')
    total_amount = subtotal + shipping_cost
    
    context = {
        'cart_items': cart_items,
        'form': form,
        'saved_addresses': saved_addresses,
        'requires_prescription': requires_prescription,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'shipping_cost': shipping_cost,
        'total_amount': total_amount,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def prescription_upload(request, order_id):
    """Upload prescription for order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        prescription_image = request.FILES.get('prescription_image')
        doctor_name = request.POST.get('doctor_name')
        doctor_license = request.POST.get('doctor_license', '')
        prescription_date = request.POST.get('prescription_date')
        notes = request.POST.get('notes', '')
        
        if prescription_image and doctor_name and prescription_date:
            # Create prescription record
            prescription = Prescription.objects.create(
                user=request.user,
                medicine=order.items.first().medicine,  # For simplicity, using first medicine
                prescription_image=prescription_image,
                doctor_name=doctor_name,
                doctor_license=doctor_license,
                prescription_date=prescription_date,
                notes=notes,
                status='pending'
            )
            
            # Update order with prescription
            order.prescription = prescription
            order.save()
            
            messages.success(request, 'Prescription uploaded successfully. It will be reviewed shortly.')
            return redirect('orders:order_detail', order_id=order.id)
        else:
            messages.error(request, 'Please fill all required fields.')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/prescription_upload.html', context)


@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            medicine = Medicine.objects.get(name=item.medicine_name)
            medicine.stock_quantity += item.quantity
            medicine.save()
        
        # Handle refund for paid orders
        if order.payment_status == 'paid':
            from payments.models import Payment, Refund
            
            # Get or create payment record
            try:
                payment = Payment.objects.get(order=order)
            except Payment.DoesNotExist:
                payment = Payment.objects.create(
                    order=order,
                    user=request.user,
                    amount=order.total_amount,
                    payment_method=order.payment_method,
                    status='completed'
                )
            
            # Create automatic refund request
            Refund.objects.create(
                payment=payment,
                amount=order.total_amount,
                reason='Order cancelled by customer',
                status='pending'
            )
            
            order.payment_status = 'refunded'
            order.save()
            
            messages.success(request, 'Order cancelled successfully. Your refund request has been submitted and will be processed within 5-7 business days.')
        else:
            messages.success(request, 'Order cancelled successfully.')
        
        # Create status history
        OrderStatusHistory.objects.create(
            order=order,
            status='cancelled',
            notes='Order cancelled by customer',
            changed_by=request.user
        )
    else:
        messages.error(request, 'This order cannot be cancelled. Orders can only be cancelled before shipping.')
    
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def shipping_addresses(request):
    """Manage shipping addresses"""
    addresses = ShippingAddress.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('orders:shipping_addresses')
    else:
        form = ShippingAddressForm()
    
    context = {
        'addresses': addresses,
        'form': form,
    }
    return render(request, 'orders/shipping_addresses.html', context)


@login_required
def delete_address(request, address_id):
    """Delete shipping address"""
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('orders:shipping_addresses')


@login_required
def set_default_address(request, address_id):
    """Set default shipping address"""
    address = get_object_or_404(ShippingAddress, id=address_id, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, 'Default address updated.')
    return redirect('orders:shipping_addresses')


# Admin views for order management
@login_required
def admin_order_list(request):
    """Admin view for all orders"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'orders/admin_order_list.html', context)


@login_required
def admin_order_detail(request, order_id):
    """Admin view for order details"""
    if not is_secure_admin(request.user):
        messages.error(request, 'Access denied.')
        return redirect('products:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status and new_status != order.status:
            old_status = order.status
            order.status = new_status
            
            # Update timestamps based on status
            if new_status == 'confirmed':
                order.confirmed_at = timezone.now()
            elif new_status == 'shipped':
                order.shipped_at = timezone.now()
            elif new_status == 'delivered':
                order.delivered_at = timezone.now()
            
            order.save()
            
            # Create status history
            OrderStatusHistory.objects.create(
                order=order,
                status=new_status,
                notes=notes,
                changed_by=request.user
            )
            
            messages.success(request, f'Order status updated from {old_status} to {new_status}.')
            return redirect('orders:admin_order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'orders/admin_order_detail.html', context)


@login_required
def prescription_review(request, prescription_id):
    """Review prescription (admin/pharmacy only)"""
    if not (request.user.is_staff or request.user.user_type == 'pharmacy'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        review_notes = request.POST.get('review_notes', '')
        
        if action == 'approve':
            prescription.status = 'approved'
            prescription.reviewed_by = request.user
            prescription.review_notes = review_notes
            prescription.save()
            
            # Update related order
            if prescription.orders.exists():
                order = prescription.orders.first()
                order.prescription_verified = True
                order.save()
            
            messages.success(request, 'Prescription approved.')
        elif action == 'reject':
            prescription.status = 'rejected'
            prescription.reviewed_by = request.user
            prescription.review_notes = review_notes
            prescription.save()
            
            messages.success(request, 'Prescription rejected.')
        
        return redirect('orders:prescription_review', prescription_id=prescription.id)
    
    context = {
        'prescription': prescription,
    }
    return render(request, 'orders/prescription_review.html', context)