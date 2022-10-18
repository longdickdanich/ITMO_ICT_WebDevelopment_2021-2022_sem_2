import copy

from django.db.models.signals import post_save, pre_save, post_init, post_delete
from django.dispatch import receiver

from hotel_app.models import Cleaner


@receiver(post_save, sender=Cleaner)
def save_logic(sender, instance, created, **kwargs):
    if created:
        print("Some logic")


@receiver(pre_save, sender=Cleaner)
def update(sender, instance, **kwargs):
    try:
        prev_instance = Cleaner.objects.get(id=instance.id)
        instance.old_phone = prev_instance.phone
    except:
        pass



@receiver(post_delete, sender=Cleaner)
def delete_log(sender, instance, **kwargs):
    print(f"Delete {instance.full_name}")
