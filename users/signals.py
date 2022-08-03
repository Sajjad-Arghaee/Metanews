from django.db.models.signals import post_save, post_delete
from .models import User, Profile
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            name=instance.username,
            email=instance.email
        )
        subject = 'Welcome to MetaNews Website'
        message = f'Glad to see you, {profile.name}'
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
