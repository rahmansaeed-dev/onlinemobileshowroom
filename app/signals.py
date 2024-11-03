# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from app.models import CustomUser  

@receiver(post_save, sender=CustomUser)  
def show_welcome_message(sender, instance, created, **kwargs):
    if created:
        messages.success(instance, 'Welcome to the site! Your account has been successfully created.')
