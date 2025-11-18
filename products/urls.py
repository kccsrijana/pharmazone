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
]
