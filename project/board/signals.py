from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad, Response
from django.conf import settings
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'


@receiver(post_save, sender=Response)
def responce_created(instance, **kwargs):
    ad = instance.ad
    author = ad.user
    email_from = settings.DEFAULT_FROM_EMAIL
    subject = "New responce"
    message = (f"Новый ответ на ваше объявление '{ad.title}' категории '{ad.category}'. Зайдите в личный кабинет чтобы "
               f"его увидеть")
    send_mail(subject, message, email_from, [author.email])


@receiver(post_save, sender=Response)
def send_response_accepted_notification(instance, **kwargs):
    if instance.accepted is True:
        ad = instance.ad
        author = instance.user
        email_from = settings.DEFAULT_FROM_EMAIL
        subject = "Responce accepted!"
        message = f"Ваш отклик на объявление '{ad.title}' категории '{ad.category}' принят"
        send_mail(subject, message, email_from, [author.email])