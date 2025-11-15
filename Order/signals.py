from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Factor
from .tasks import update_status_after_5_minutes
#
# @receiver(post_save, sender=Factor)
# def schedule_job(sender, instance, created, **kwargs):
#     if created:
#         update_status_after_5_minutes.apply_async((instance.id,), countdown=300)
