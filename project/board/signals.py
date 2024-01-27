from django.core.mail import send_mail, EmailMultiAlternatives
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
    subject = "Новый отклик"
    message = (f"Новый отклик на ваше объявление '{ad.title}' категории '{ad.category}'. Зайдите в личный кабинет чтобы "
               f"его увидеть")
    msg = EmailMultiAlternatives(subject, message, email_from, [author.email])
    html_content = f"""
    <h1>Новый отклик</h1>
    <p>На ваше объявление '{ad.title}' категории '{ad.category}' поступил новый отклик.</p>
    <p>Чтобы его увидеть, зайдите в личный кабинет.</p>
    """
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Response)
def send_response_accepted_notification(instance, **kwargs):
    if instance.accepted is True:
        ad = instance.ad
        author = instance.user
        email_from = settings.DEFAULT_FROM_EMAIL
        subject = "Отклик принят!"
        message = f"Ваш отклик на объявление '{ad.title}' категории '{ad.category}' принят"
        msg = EmailMultiAlternatives(subject, message, email_from, [author.email])
        html_content = f"""
        <h1>Отклик принят!</h1>
        <p>Ваш отклик на объявление '{ad.title}' категории '{ad.category}' принят.</p>
        """
        msg.attach_alternative(html_content, "text/html")
        msg.send()