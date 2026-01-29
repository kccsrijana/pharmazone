from django.urls import path
from . import views

app_name = 'pharmacist_chat'

urlpatterns = [
    # Customer URLs
    path('', views.ask_pharmacist_home, name='home'),
    path('start/', views.start_chat, name='start_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('my-chats/', views.my_chats, name='my_chats'),
    path('close/<int:chat_id>/', views.close_chat, name='close_chat'),
    path('quick-response/<int:response_id>/', views.quick_response_detail, name='quick_response'),
    
    # Pharmacist URLs
    path('pharmacist/', views.pharmacist_dashboard, name='pharmacist_dashboard'),
    path('pharmacist/chat/<int:chat_id>/', views.pharmacist_chat_detail, name='pharmacist_chat_detail'),
]