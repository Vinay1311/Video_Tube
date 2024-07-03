#--------------- External Imports ----------------- #

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

#--------------- Internal Imports ----------------- #
from app_users.models import UserDetails
from YT_Project.settings import EMAIL_HOST_USER
from helper.function import generate_unique_login_link

@receiver(post_save, sender = UserDetails)
def send_email(sender, instance, created, **kwargs):
    if created:
        subject = f'Confirmation Mail from YT_Team'
        message = f'Hey {instance.fullname}, Thank You to Register Yourself on the YT_Project \nUse below link to go to Login Page: \n{generate_unique_login_link(instance.username)} '
        sender = EMAIL_HOST_USER
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, sender, recipient_list)
            print(f"Email sent successfully to {instance.email}")
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {e}")
        