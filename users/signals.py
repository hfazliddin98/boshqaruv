from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Users, Struktura

# @receiver(post_save, sender=Users)
# def set_parol_on_save(sender, instance, created, **kwargs):
#     if instance.password and instance.parol != instance.password:
#         instance.parol = instance.password
#         instance.save(update_fields=['parol'])


def safe_delete_pattern(pattern):
    """Cache pattern delete - LocMemCache uchun safe version"""
    try:
        if hasattr(cache, 'delete_pattern'):
            cache.delete_pattern(pattern)
        else:
            # LocMemCache uchun barcha cache ni tozalash
            cache.clear()
    except Exception:
        # Xato bo'lsa ham ishni davom ettirish
        pass


@receiver([post_save, post_delete], sender=Users)
def invalidate_user_cache(sender, **kwargs):
    """Users model o'zgarsa cache'ni tozalash"""
    safe_delete_pattern('admin_user_stats_*')


@receiver([post_save, post_delete], sender=Struktura)
def invalidate_struktura_cache(sender, **kwargs):
    """Struktura model o'zgarsa cache'ni tozalash"""
    safe_delete_pattern('admin_user_stats_*')
    safe_delete_pattern('admin_struktura_stats_*')