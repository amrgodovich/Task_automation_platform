from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
# Import generic libraries for other channels if needed (e.g., slack_sdk)

@shared_task
def send_notification_task(channel, recipients, subject, body):
    """
    This runs in the background (Redis/Celery).
    It does NOT touch the database models directly if possible.
    It just takes strings/lists and executes.
    """
    try:
        print(f"🚀 Celery Worker: Sending {channel} to {recipients}")
        
        if channel == 'EMAIL':
            # Django's built-in emailer
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )
            
        elif channel == 'IN_APP':
            # For In-App, we might need to save to DB, 
            # so we might import a Notification model here.
            # Notification.objects.create(...)
            pass

    except Exception as e:
        # Celery logs this automatically, but good to be explicit
        print(f"❌ Task Failed: {e}")