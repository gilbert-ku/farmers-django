from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views  # This should work now

urlpatterns = [
    # Authentication
    path('api/auth/register/agrovet/', views.AgrovetRegistrationView.as_view(), name='agrovet_register'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/password-reset/', views.password_reset_view, name='password_reset'),
    path('api/auth/profile/', views.user_profile_view, name='user_profile'),
    
    # Agrovet
    path('api/agrovet/dashboard/', views.agrovet_dashboard_view, name='agrovet_dashboard'),
    path('api/agrovet/register-farmer/', views.register_farmer_view, name='register_farmer'),
    
    # Farmer
    path('api/farmer/dashboard/', views.farmer_dashboard_view, name='farmer_dashboard'),
]