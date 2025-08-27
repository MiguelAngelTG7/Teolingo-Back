from django.test import TestCase
from django.core.mail import send_mail
from django.conf import settings

class EmailTest(TestCase):
    def test_send_email(self):
        """Test sending an email"""
        subject = 'Test Email'
        message = 'This is a test email from Django.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['test@example.com']  # Replace with your test email
        
        # Send email
        result = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        
        # Check if email was sent successfully
        self.assertEqual(result, 1)
