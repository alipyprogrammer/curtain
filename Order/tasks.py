# your_app/tasks.py
from celery import shared_task
from .models import Factor

@shared_task
def update_status_after_5_minutes(factor_id):
    try:
        factor = Factor.objects.get(id=factor_id)
        if factor.status_code == 4 :
            factor.status_code = 0
            factor.save()
    except Factor.DoesNotExist:
        pass
