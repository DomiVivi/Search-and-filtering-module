from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import EducationalMaterial, Cache


@receiver(post_save, sender=EducationalMaterial)
@receiver(post_delete, sender=EducationalMaterial)
def clear_cache_on_save(sender, instance, **kwargs):
    Cache.objects.all().delete()
