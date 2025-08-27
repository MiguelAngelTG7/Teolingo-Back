from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegistroView, 
    TestEmailView,
    VerificarEmailView,
    SolicitarResetPasswordView,
    ResetPasswordView,
    CustomTokenObtainPairView
)

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verificar-email/', VerificarEmailView.as_view(), name='verificar-email'),
    path('solicitar-reset-password/', SolicitarResetPasswordView.as_view(), name='solicitar-reset-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('test-email/', TestEmailView.as_view(), name='test-email'),
]