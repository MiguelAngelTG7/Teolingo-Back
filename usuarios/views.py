from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.db import transaction
from .serializers import CustomTokenObtainPairSerializer
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from datetime import timedelta
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer
from .models import Usuario
from .utils import send_async_mail
import logging

logger = logging.getLogger('django.mail')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegistroView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                verification_url = f"{settings.FRONTEND_URL}/verificar-email/{user.token_verificacion}"
                
                # Log antes de enviar el email
                logger.debug(f"Intentando enviar email a: {user.email}")
                
                try:
                    send_mail(
                        'Verifica tu cuenta de Teolingo',
                        f'Hola {user.nombre_completo},\n\nPor favor verifica tu cuenta haciendo clic aquí.',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    logger.debug(f"Email enviado exitosamente a {user.email}")
                except Exception as e:
                    logger.error(f"Error enviando email: {str(e)}")
                    # Aún así retornamos éxito al usuario
                
                return Response({
                    'message': 'Usuario registrado exitosamente. Por favor verifica tu correo electrónico.',
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error en registro: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerfilView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificarEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(token_verificacion=token)
            
            # Verificar si el token no ha expirado (24 horas)
            if user.token_verificacion_fecha < timezone.now() - timedelta(days=1):
                return Response({'error': 'El token ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.email_verificado = True
            user.token_verificacion = None
            user.token_verificacion_fecha = None
            user.save()

            return Response({'message': 'Email verificado correctamente'})
        except Usuario.DoesNotExist:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

class SolicitarResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = Usuario.objects.get(email=email)
            
            # Generar token de reset
            token = get_random_string(64)
            user.token_reset_password = token
            user.token_reset_password_fecha = timezone.now()
            user.save()

            # Enviar correo
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
            subject = 'Recuperación de contraseña - Teolingo'
            message = f'''
            Hola {user.nombre_completo},

            Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña:

            {reset_url}

            Este enlace expirará en 1 hora.

            Si no solicitaste este cambio, puedes ignorar este correo.

            Saludos,
            El equipo de Teolingo
            '''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'Se ha enviado un correo con las instrucciones para restablecer tu contraseña'})
        except Usuario.DoesNotExist:
            # Por seguridad, no revelamos si el email existe o no
            return Response({'message': 'Si el correo existe en nuestra base de datos, recibirás las instrucciones para restablecer tu contraseña'})

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('password')

        if not token or not new_password:
            return Response({'error': 'Token y nueva contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(token_reset_password=token)
            
            # Verificar si el token no ha expirado (1 hora)
            if user.token_reset_password_fecha < timezone.now() - timedelta(hours=1):
                return Response({'error': 'El token ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.token_reset_password = None
            user.token_reset_password_fecha = None
            user.is_active = True
            user.email_verificado = True
            user.save()

            return Response({'message': 'Contraseña actualizada correctamente'})
        except Usuario.DoesNotExist:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

class TestEmailView(APIView):
    permission_classes = [AllowAny]  # Solo para pruebas, cambiar a IsAuthenticated en producción

    def post(self, request):
        try:
            subject = 'Test Email from Teolingo'
            message = 'If you receive this email, the email configuration is working correctly!'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.data.get('email', '')]  # El email se debe enviar en el body de la petición
            
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            
            return Response({
                'message': 'Email sent successfully',
                'to': recipient_list[0]
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
