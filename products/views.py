from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Medicine, Manufacturer, MedicineReview
from .forms import MedicineReviewForm


def home_view(request):
    """Home page view"""
    # Get featured medicines
    featured_medicines = Medicine.objects.filter(
        is_featured=True, 
        is_active=True
    )[:8]
    
    # Get categories
    categories = Category.objects.filter(is_active=True)[:6]
    
    # Get recent medicines
    recent_medicines = Medicine.objects.filter(
        is_active=True
    ).order_by('-created_at')[:8]
    
    context = {
        'featured_medicines': featured_medicines,
        'categories': categories,
        'recent_medicines': recent_medicines,
    }
    return render(request, 'products/home.html', context)


def medicine_list_view(request):
    """Medicine listing view with search and filters"""
    medicines = Medicine.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(generic_name__icontains=search_query) |
            Q(composition__icontains=search_query) |
            Q(indications__icontains=search_query)
        )
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        medicines = medicines.filter(category_id=category_id)
    
    # Manufacturer filter
    manufacturer_id = request.GET.get('manufacturer')
    if manufacturer_id:
        medicines = medicines.filter(manufacturer_id=manufacturer_id)
    
    # Prescription type filter
    prescription_type = request.GET.get('prescription_type')
    if prescription_type:
        medicines = medicines.filter(prescription_type=prescription_type)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        medicines = medicines.filter(price__gte=min_price)
    if max_price:
        medicines = medicines.filter(price__lte=max_price)
    
    # Sort by
    sort_by = request.GET.get('sort_by', 'name')
    if sort_by == 'price_low':
        medicines = medicines.order_by('price')
    elif sort_by == 'price_high':
        medicines = medicines.order_by('-price')
    elif sort_by == 'name':
        medicines = medicines.order_by('name')
    elif sort_by == 'newest':
        medicines = medicines.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(medicines, 12)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    
    # Get filter options
    categories = Category.objects.filter(is_active=True)
    manufacturers = Manufacturer.objects.all()
    
    context = {
        'medicines': medicines,
        'categories': categories,
        'manufacturers': manufacturers,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_manufacturer': manufacturer_id,
        'selected_prescription_type': prescription_type,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'products/medicine_list.html', context)


def medicine_detail_view(request, slug):
    """Medicine detail view"""
    medicine = get_object_or_404(Medicine, slug=slug, is_active=True)
    
    # Get reviews
    reviews = MedicineReview.objects.filter(medicine=medicine).order_by('-created_at')
    
    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Get related medicines
    related_medicines = Medicine.objects.filter(
        category=medicine.category,
        is_active=True
    ).exclude(id=medicine.id)[:4]
    
    # Check if user has already reviewed this medicine
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = MedicineReview.objects.get(medicine=medicine, user=request.user)
        except MedicineReview.DoesNotExist:
            pass
    
    context = {
        'medicine': medicine,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_medicines': related_medicines,
        'user_review': user_review,
    }
    return render(request, 'products/medicine_detail.html', context)


def category_list_view(request):
    """Category listing view"""
    categories = Category.objects.filter(is_active=True)
    context = {
        'categories': categories,
    }
    return render(request, 'products/category_list.html', context)


def category_detail_view(request, slug):
    """Category detail view"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    medicines = Medicine.objects.filter(
        category=category,
        is_active=True
    ).order_by('name')
    
    # Pagination
    paginator = Paginator(medicines, 12)
    page_number = request.GET.get('page')
    medicines = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'medicines': medicines,
    }
    return render(request, 'products/category_detail.html', context)


@login_required
def add_review(request, medicine_id):
    """Add medicine review"""
    medicine = get_object_or_404(Medicine, id=medicine_id, is_active=True)
    
    if request.method == 'POST':
        form = MedicineReviewForm(request.POST)
        if form.is_valid():
            # Check if user already reviewed this medicine
            if MedicineReview.objects.filter(medicine=medicine, user=request.user).exists():
                messages.error(request, 'You have already reviewed this medicine.')
                return redirect('medicine_detail', slug=medicine.slug)
            
            review = form.save(commit=False)
            review.medicine = medicine
            review.user = request.user
            review.save()
            
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('medicine_detail', slug=medicine.slug)
    else:
        form = MedicineReviewForm()
    
    context = {
        'form': form,
        'medicine': medicine,
    }
    return render(request, 'products/add_review.html', context)


@csrf_exempt
def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        if len(query) >= 2:
            medicines = Medicine.objects.filter(
                Q(name__icontains=query) |
                Q(generic_name__icontains=query)
            ).filter(is_active=True)[:5]
            
            suggestions = []
            for medicine in medicines:
                suggestions.append({
                    'name': medicine.name,
                    'slug': medicine.slug,
                    'strength': medicine.strength,
                    'price': float(medicine.current_price),
                })
            
            return JsonResponse({'suggestions': suggestions})
    
    return JsonResponse({'suggestions': []})