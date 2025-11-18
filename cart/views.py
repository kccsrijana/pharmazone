from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from products.models import Medicine
from .models import Cart, CartItem


@login_required
def cart_view(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    # Calculate totals
    from decimal import Decimal
    subtotal = float(cart.total_price) if cart.total_price else 0.0
    tax_amount = 0.0  # No tax
    shipping_cost = 0.0 if subtotal >= 2000 else 100.0
    total_amount = round(subtotal + shipping_cost, 2)
    free_shipping_threshold = 2000.0
    amount_needed_for_free_shipping = max(0, round(free_shipping_threshold - subtotal, 2))
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'shipping_cost': shipping_cost,
        'total_amount': total_amount,
        'amount_needed_for_free_shipping': amount_needed_for_free_shipping,
    }
    return render(request, 'cart/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, medicine_id):
    """Add medicine to cart"""
    medicine = get_object_or_404(Medicine, id=medicine_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if medicine is in stock
    if medicine.stock_quantity < quantity:
        messages.error(request, f'Only {medicine.stock_quantity} items available in stock.')
        return redirect('products:medicine_detail', slug=medicine.slug)
    
    # Check quantity limits
    if quantity < medicine.min_order_quantity:
        messages.error(request, f'Minimum order quantity is {medicine.min_order_quantity}.')
        return redirect('products:medicine_detail', slug=medicine.slug)
    
    if quantity > medicine.max_order_quantity:
        messages.error(request, f'Maximum order quantity is {medicine.max_order_quantity}.')
        return redirect('products:medicine_detail', slug=medicine.slug)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update existing item
        new_quantity = cart_item.quantity + quantity
        
        # Check stock again
        if medicine.stock_quantity < new_quantity:
            messages.error(request, f'Only {medicine.stock_quantity} items available in stock.')
            return redirect('products:medicine_detail', slug=medicine.slug)
        
        # Check max quantity
        if new_quantity > medicine.max_order_quantity:
            messages.error(request, f'Maximum order quantity is {medicine.max_order_quantity}.')
            return redirect('products:medicine_detail', slug=medicine.slug)
        
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Updated {medicine.name} quantity in cart.')
    else:
        messages.success(request, f'{medicine.name} added to cart.')
    
    return redirect('cart:cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    # Check quantity limits
    if quantity < cart_item.medicine.min_order_quantity:
        messages.error(request, f'Minimum order quantity is {cart_item.medicine.min_order_quantity}.')
        return redirect('cart:cart')
    
    if quantity > cart_item.medicine.max_order_quantity:
        messages.error(request, f'Maximum order quantity is {cart_item.medicine.max_order_quantity}.')
        return redirect('cart:cart')
    
    # Check stock
    if cart_item.medicine.stock_quantity < quantity:
        messages.error(request, f'Only {cart_item.medicine.stock_quantity} items available in stock.')
        return redirect('cart:cart')
    
    cart_item.quantity = quantity
    cart_item.save()
    
    messages.success(request, f'Updated {cart_item.medicine.name} quantity.')
    return redirect('cart:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        medicine_name = cart_item.medicine.name
        cart_item.delete()
        
        messages.success(request, f'{medicine_name} removed from cart.')
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
    
    return redirect('cart:cart')


@login_required
@require_POST
def clear_cart(request):
    """Clear entire cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    
    messages.success(request, 'Cart cleared successfully.')
    return redirect('cart:cart')


@login_required
@csrf_exempt
def cart_count(request):
    """AJAX endpoint to get cart item count"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.total_items
    else:
        count = 0
    
    return JsonResponse({'count': count})


@login_required
@csrf_exempt
def add_to_cart_ajax(request, medicine_id):
    """AJAX endpoint to add item to cart"""
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, id=medicine_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if medicine is in stock
        if medicine.stock_quantity < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {medicine.stock_quantity} items available in stock.'
            })
        
        # Check quantity limits
        if quantity < medicine.min_order_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Minimum order quantity is {medicine.min_order_quantity}.'
            })
        
        if quantity > medicine.max_order_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Maximum order quantity is {medicine.max_order_quantity}.'
            })
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            medicine=medicine,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update existing item
            new_quantity = cart_item.quantity + quantity
            
            # Check stock again
            if medicine.stock_quantity < new_quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {medicine.stock_quantity} items available in stock.'
                })
            
            # Check max quantity
            if new_quantity > medicine.max_order_quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Maximum order quantity is {medicine.max_order_quantity}.'
                })
            
            cart_item.quantity = new_quantity
            cart_item.save()
            message = f'Updated {medicine.name} quantity in cart.'
        else:
            message = f'{medicine.name} added to cart.'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})