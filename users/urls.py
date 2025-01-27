from django.urls import path
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, CustomTokenObtainPairView, admin_dashboard, user_profile, dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', ratelimit(key='ip', rate='5/m', method='POST')(CustomTokenObtainPairView.as_view()), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('profile/', user_profile, name='user_profile'),
    path('dashboard/', dashboard, name='dashboard'),
]