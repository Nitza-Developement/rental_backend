from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from rental.models import Contract, StageUpdate


@receiver(post_save, sender=Contract)
def update_active_date(sender, instance, **kwargs):
    if kwargs.get('update_fields') and 'stage' in kwargs['update_fields']:
        if instance.stage == StageUpdate.ACTIVE:
            instance.active_date = timezone.now()
            instance.save(update_fields=['active_date'])


@receiver(post_save, sender=Contract)
def update_end_date(sender, instance, **kwargs):
    if kwargs.get('update_fields') and 'stage' in kwargs['update_fields']:
        if instance.stage == StageUpdate.ENDED:
            instance.end_date = timezone.now()
            instance.save(update_fields=['end_date'])
