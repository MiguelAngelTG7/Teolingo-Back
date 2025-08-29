from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegistroView,
    CustomTokenObtainPairView
)

app_name = 'usuarios'  # Add namespace for better URL organization

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]