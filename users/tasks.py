from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(email):
    send_mail(
        subject='Welcome to our platform!',
        message='Hi there! Thanks for registering.',
        from_email='your_email@example.com',
        recipient_list=[email],
    )
    return f"Email sent to {email}"
