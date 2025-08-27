from django.urls import reverse
from django.utils import timezone
from .models import Xabarnoma

class XabarnomaService:
    """Bildirishnoma xizmatlari"""
    
    @staticmethod
    def create_notification(recipient, title, message, notification_type, sender=None, **kwargs):
        """Yangi bildirishnoma yaratish"""
        return Xabarnoma.objects.create(
            recipient=recipient,
            sender=sender,
            title=title,
            message=message,
            notification_type=notification_type,
            **kwargs
        )
    
    @staticmethod
    def notify_new_topshiriq(topshiriq):
        """Yangi topshiriq haqida xabar berish"""
        try:
            action_url = f"/topshiriq/{topshiriq.pk}/"
            
            XabarnomaService.create_notification(
                recipient=topshiriq.bajaruvchi_user,
                sender=topshiriq.yaratuvchi_user,
                title="📋 Yangi topshiriq berildi",
                message=f"Sizga '{topshiriq.title}' nomli yangi topshiriq berildi. Iltimos, topshiriqni ko'rib chiqing.",
                notification_type='topshiriq_yangi',
                topshiriq=topshiriq,
                action_url=action_url,
                priority='high'
            )
            print(f"✅ Yangi topshiriq bildirishnomasi yuborildi: {topshiriq.bajaruvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Topshiriq bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def notify_topshiriq_javob(javob):
        """Topshiriq javobi haqida xabar berish"""
        try:
            action_url = f"/topshiriq/baxolash/{javob.topshiriq.pk}/"
            
            XabarnomaService.create_notification(
                recipient=javob.topshiriq.yaratuvchi_user,
                sender=javob.bajaruvchi_user,
                title="💬 Topshiriq javobi keldi",
                message=f"'{javob.topshiriq.title}' topshirig'iga {javob.bajaruvchi_user.get_full_name()} tomonidan javob yuborildi. Javobni ko'rib chiqing va baholang.",
                notification_type='topshiriq_javob',
                topshiriq=javob.topshiriq,
                javob=javob,
                action_url=action_url,
                priority='high'
            )
            print(f"✅ Javob bildirishnomasi yuborildi: {javob.topshiriq.yaratuvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Javob bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def notify_topshiriq_baholandi(topshiriq):
        """Topshiriq baholandi haqida xabar berish"""
        try:
            action_url = f"/topshiriq/{topshiriq.pk}/"
            baho_display = topshiriq.get_baxo_display() if topshiriq.baxo else "Noma'lum"
            status_display = topshiriq.get_status_display() if topshiriq.status else "Noma'lum"
            
            XabarnomaService.create_notification(
                recipient=topshiriq.bajaruvchi_user,
                sender=topshiriq.yaratuvchi_user,
                title="⭐ Topshiriq baholandi",
                message=f"'{topshiriq.title}' topshirig'ingiz baholandi.\n📊 Baho: {baho_display}\n📝 Holat: {status_display}",
                notification_type='topshiriq_baholandi',
                topshiriq=topshiriq,
                action_url=action_url,
                priority='normal'
            )
            print(f"✅ Baholash bildirishnomasi yuborildi: {topshiriq.bajaruvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Baholash bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def mark_all_as_read(user):
        """Foydalanuvchining barcha bildirishnomalarini o'qilgan deb belgilash"""
        unread_notifications = user.xabarlar.filter(is_read=False)
        count = unread_notifications.count()
        unread_notifications.update(is_read=True, read_at=timezone.now())
        return count
    
    @staticmethod
    def get_unread_count(user):
        """O'qilmagan bildirishnomalar sonini olish"""
        return user.xabarlar.filter(is_read=False).count()
    
    @staticmethod
    def get_recent_notifications(user, limit=5):
        """So'nggi bildirishnomalarni olish"""
        return user.xabarlar.filter(is_read=False)[:limit]
