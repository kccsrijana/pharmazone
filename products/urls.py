from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('medicines/', views.medicine_list_view, name='medicine_list'),
    path('medicine/<slug:slug>/', views.medicine_detail_view, name='medicine_detail'),
    path('categories/', views.category_list_view, name='category_list'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('medicine/<int:medicine_id>/review/', views.add_review, name='add_review'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    
    # Admin Medicine Management URLs
    path('admin/medicines/', views.admin_medicine_list, name='admin_medicine_list'),
    path('admin/medicine/<int:medicine_id>/', views.admin_medicine_detail, name='admin_medicine_detail'),
    path('admin/medicine/add/', views.admin_medicine_add, name='admin_medicine_add'),
    path('admin/medicine/<int:medicine_id>/edit/', views.admin_medicine_edit, name='admin_medicine_edit'),
    path('admin/medicine/<int:medicine_id>/delete/', views.admin_medicine_delete, name='admin_medicine_delete'),
    path('admin/medicine/<int:medicine_id>/toggle-status/', views.admin_medicine_toggle_status, name='admin_medicine_toggle_status'),
    path('admin/medicine/<int:medicine_id>/toggle-featured/', views.admin_medicine_toggle_featured, name='admin_medicine_toggle_featured'),
    
    # Admin Category Management URLs
    path('admin/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin/category/add/', views.admin_category_add, name='admin_category_add'),
    path('admin/category/<int:category_id>/edit/', views.admin_category_edit, name='admin_category_edit'),
    
    # Admin Manufacturer Management URLs
    path('admin/manufacturers/', views.admin_manufacturer_list, name='admin_manufacturer_list'),
    path('admin/manufacturer/add/', views.admin_manufacturer_add, name='admin_manufacturer_add'),
]
