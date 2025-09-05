from django.urls import reverse
from django.utils import timezone
from .models import Notification

class NotificationService:
    """Bildirishnoma xizmatlari"""
    
    @staticmethod
    def create_notification(user, topshiriq):
        """Yangi bildirishnoma yaratish"""
        return Notification.objects.create(
            users=user,
            topshiriq=topshiriq
        )
    
    @staticmethod
    def notify_new_topshiriq(topshiriq):
        """Yangi topshiriq haqida xabar berish"""
        try:
            NotificationService.create_notification(
                user=topshiriq.bajaruvchi_user,
                topshiriq=topshiriq
            )
            print(f"✅ Yangi topshiriq bildirishnomasi yuborildi: {topshiriq.bajaruvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Topshiriq bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def notify_topshiriq_javob(javob):
        """Topshiriq javobi haqida xabar berish"""
        try:
            NotificationService.create_notification(
                user=javob.topshiriq.yaratuvchi_user,
                topshiriq=javob.topshiriq
            )
            print(f"✅ Javob bildirishnomasi yuborildi: {javob.topshiriq.yaratuvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Javob bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def notify_topshiriq_baholandi(topshiriq):
        """Topshiriq baholandi haqida xabar berish"""
        try:
            NotificationService.create_notification(
                user=topshiriq.bajaruvchi_user,
                topshiriq=topshiriq
            )
            print(f"✅ Baholash bildirishnomasi yuborildi: {topshiriq.bajaruvchi_user.get_full_name()}")
            
        except Exception as e:
            print(f"❌ Baholash bildirishnomasi yuborishda xatolik: {e}")
    
    @staticmethod
    def mark_all_as_read(user):
        """Foydalanuvchining barcha bildirishnomalarini o'qilgan deb belgilash"""
        unread_notifications = user.bildirishnomalar.filter(is_read=False)
        count = unread_notifications.count()
        unread_notifications.update(is_read=True)
        return count
    
    @staticmethod
    def get_unread_count(user):
        """O'qilmagan bildirishnomalar sonini olish"""
        return user.bildirishnomalar.filter(is_read=False).count()
    
    @staticmethod
    def get_recent_notifications(user, limit=5):
        """So'nggi bildirishnomalarni olish"""
        return user.bildirishnomalar.all().order_by('-created_at')[:limit]
