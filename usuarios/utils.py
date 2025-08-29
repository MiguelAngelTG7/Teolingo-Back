from django.core.mail import send_mail
from django.conf import settings
from threading import Thread

def send_async_mail(subject, message, recipient_list):
    def _send_mail():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    email_thread = Thread(target=_send_mail)
    email_thread.start()