from django.db import models
from users.models import AsosiyModel, Users
from topshiriq.choices import StatusChoice, XolatChoice
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Topshiriq(AsosiyModel):
    yaratuvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='yaratuvchi_user_topshiriqlar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='bajaruvchi_user_topshiriqlar')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=XolatChoice.choices, default=XolatChoice.ODDIY)
    baxo = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, help_text="Baho 0 dan 100 gacha qiymat qabul qiladi")
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    javob_yuborildi = models.BooleanField(default=False)  
    urinishlar_soni = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)  
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Topshiriq #{self.pk}"
    
    def get_baxo_description(self):
        """Baxo sonini matn tavsifi bilan qaytaradi"""
        if self.baxo >= 90:
            return f"{self.baxo} ball (A'lo)"
        elif self.baxo >= 80:
            return f"{self.baxo} ball (Yaxshi)"
        elif self.baxo >= 70:
            return f"{self.baxo} ball (Qoniqarli)"
        elif self.baxo >= 60:
            return f"{self.baxo} ball (O'rtacha)"
        else:
            return f"{self.baxo} ball (Qoniqarsiz)"

    class Meta:
        indexes = [
            models.Index(fields=['yaratuvchi_user']),        # Yaratgan user bo'yicha
            models.Index(fields=['bajaruvchi_user']),         # Bajaruvchi bo'yicha
            models.Index(fields=['status']),                   # Holat bo'yicha
            models.Index(fields=['javob_yuborildi']),                   # Javob yuborilganligi bo'yicha
            models.Index(fields=['boshlanish_vaqti']),          # Sana bo'yicha
        ]


class TopshiriqFile(AsosiyModel):
    topshiriq = models.ForeignKey(Topshiriq, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='topshiriq_files/')

    def __str__(self):
        return self.file.name


class TopshiriqJavob(AsosiyModel):
    topshiriq = models.ForeignKey(Topshiriq, on_delete=models.CASCADE, related_name='javoblar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return f"Javob #{self.pk} - {self.title or self.topshiriq.title}"


class TopshiriqJavobFile(AsosiyModel):
    javob = models.ForeignKey(TopshiriqJavob, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='topshiriq_javob_files/')

    def __str__(self):
        return self.file.name


class Notification(AsosiyModel):
    """Foydalanuvchi bildirishnomalari"""
    
    NOTIFICATION_TYPES = [
        ('topshiriq_yangi', 'Yangi topshiriq'),
        ('topshiriq_javob', 'Topshiriq javobi'),
        ('topshiriq_baholandi', 'Topshiriq baholandi'),
        ('system', 'Tizim xabari'),
    ]
    
    recipient = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='xabarlar')
    sender = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='yuborilgan_xabarlar')
    
    title = models.CharField('Sarlavha', max_length=255)
    message = models.TextField('Xabar matni')
    notification_type = models.CharField('Tur', max_length=30, choices=NOTIFICATION_TYPES)
    
    # Bog'lanish obyektlari
    topshiriq = models.ForeignKey(Topshiriq, on_delete=models.CASCADE, null=True, blank=True)
    javob = models.ForeignKey(TopshiriqJavob, on_delete=models.CASCADE, null=True, blank=True)
    
    # Holat
    is_read = models.BooleanField('O\'qildi', default=False)
    
    class Meta:
        verbose_name = 'Bildirishnoma'
        verbose_name_plural = 'Bildirishnomalar'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['sender']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"
    
    def mark_as_read(self):
        """Bildirishnomani o'qilgan deb belgilash"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

