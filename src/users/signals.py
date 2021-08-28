from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import Profile
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = "Welcome to DevSearch"
        message = "We are very glad that you are here"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = instance.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# post_save.connect(profile_updated, sender=Profile)
# post_delete.connect(delete_user, sender=Profile)
post_save.connect(update_user, sender=Profile)
