from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),    
    path('status/<int:id>/', views.post_detail, name='post_detail'),    
    path('status-update/<int:id>/', views.post_update, name='post_update'),    
]
