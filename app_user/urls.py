from django.urls import path
from app_user import views


urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('change_password/', views.change_password, name='change_password'),
    # path('profile/<str:username>/', views.User_Profile.as_view(), name='profile'),
]
