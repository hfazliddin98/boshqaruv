from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users

# @receiver(post_save, sender=Users)
# def set_parol_on_save(sender, instance, created, **kwargs):
#     if instance.password and instance.parol != instance.password:
#         instance.parol = instance.password
#         instance.save(update_fields=['parol'])