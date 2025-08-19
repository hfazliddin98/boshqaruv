from django.db import models
from users.models import AsosiyModel, Users
from topshiriq.choices import TopshiriqType, StatusChoice, XolatChoice, BaxoChoice
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
    baxo = models.CharField(max_length=30, choices=BaxoChoice.choices, default=BaxoChoice.QONIQARSIZ)
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    javob_yuborildi = models.BooleanField(default=False)  
    urinishlar_soni = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)  
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Topshiriq #{self.pk}"

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


class TopshiriqReport(AsosiyModel):
    """Topshiriq hisobotlari - javobga asoslangan avtomatik hisobot"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Topshirilgan'), 
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
        ('revision', 'Qayta ko\'rishda'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    ]
    
    # Asosiy bog'lanishlar
    topshiriq = models.OneToOneField(Topshiriq, on_delete=models.CASCADE, related_name='report')
    javob = models.ForeignKey(TopshiriqJavob, on_delete=models.CASCADE, related_name='reports', null=True, blank=True)
    
    # Foydalanuvchilar
    yaratuvchi = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='created_reports')
    bajaruvchi = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='submitted_reports')
    tasdiqlovchi = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='approved_reports', null=True, blank=True)
    
    # Hisobot ma'lumotlari
    title = models.CharField('Hisobot sarlavhasi', max_length=255)
    summary = models.TextField('Qisqacha xulosа', help_text="Topshiriq va javobning qisqacha xulosasi")
    full_report = models.TextField('To\'liq hisobot', help_text="Avtomatik generatsiya qilingan to'liq hisobot")
    
    # Holat va boshqarish
    status = models.CharField('Holat', max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField('Muhimlik darajasi', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Vaqt ma'lumotlari
    deadline = models.DateTimeField('Muddat', null=True, blank=True)
    completed_at = models.DateTimeField('Bajarilgan vaqt', null=True, blank=True)
    approved_at = models.DateTimeField('Tasdiqlangan vaqt', null=True, blank=True) 
    rejected_at = models.DateTimeField('Rad etilgan vaqt', null=True, blank=True)
    
    # Qo'shimcha ma'lumotlar
    comment = models.TextField('Izoh/Fikr', blank=True, null=True, help_text="Tasdiqlovchi yoki rad etuvchining izohi")
    rating = models.PositiveSmallIntegerField('Baho', null=True, blank=True, help_text="1-5 baho")
    
    # Statistika 
    view_count = models.PositiveIntegerField('Ko\'rishlar soni', default=0)
    is_archived = models.BooleanField('Arxivlangan', default=False)
    
    class Meta:
        verbose_name = 'Topshiriq Hisoboti'
        verbose_name_plural = 'Topshiriq Hisobotlari'
        ordering = ['-created_at', '-priority']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),  
            models.Index(fields=['yaratuvchi']),
            models.Index(fields=['bajaruvchi']),
            models.Index(fields=['completed_at']),
            models.Index(fields=['is_archived']),
            models.Index(fields=['status', 'priority']),
        ]
        
    def __str__(self):
        return f"{self.title} - {self.bajaruvchi.get_full_name()}"
        
    def save(self, *args, **kwargs):
        # Avtomatik title yaratish
        if not self.title:
            self.title = f"Hisobot: {self.topshiriq.title}"
            
        # Deadline topshiriq deadline dan olish
        if not self.deadline and self.topshiriq.tugash_vaqti:
            self.deadline = self.topshiriq.tugash_vaqti
            
        # Priority topshiriq priority dan olish  
        if self.topshiriq.xolat == 'SHOSHILINCH':
            self.priority = 'urgent'
        elif self.topshiriq.xolat == 'MUHIM':
            self.priority = 'high'
            
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Muddat o'tib ketganligini tekshirish"""
        return self.deadline and timezone.now() > self.deadline and self.status in ['pending', 'completed']
    
    @property 
    def duration_days(self):
        """Bajarilish vaqtini kunlarda hisoblash"""
        if self.completed_at and self.topshiriq.boshlanish_vaqti:
            delta = self.completed_at - self.topshiriq.boshlanish_vaqti
            return delta.days
        return None
        
    def approve(self, user, comment=None):
        """Hisobotni tasdiqlash"""
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.tasdiqlovchi = user
        if comment:
            self.comment = comment
        self.save()
        
        # Topshiriq holatini yangilash
        self.topshiriq.status = 'QABUL_QILINDI'
        self.topshiriq.save()
    
    def reject(self, user, comment):
        """Hisobotni rad etish"""
        self.status = 'rejected'
        self.rejected_at = timezone.now()
        self.tasdiqlovchi = user
        self.comment = comment
        self.save()
        
        # Topshiriq holatini yangilash
        self.topshiriq.status = 'QAYTARILDI'
        self.topshiriq.save()
        
    def generate_full_report(self):
        """To'liq hisobotni avtomatik generatsiya qilish"""
        report_parts = []
        
        # Topshiriq ma'lumotlari
        report_parts.append("=== TOPSHIRIQ MA'LUMOTLARI ===")
        report_parts.append(f"Sarlavha: {self.topshiriq.title}")
        report_parts.append(f"Yaratuvchi: {self.yaratuvchi.get_full_name()}")
        report_parts.append(f"Bajaruvchi: {self.bajaruvchi.get_full_name()}")
        report_parts.append(f"Yaratilgan: {self.topshiriq.created_at.strftime('%Y-%m-%d %H:%M')}")
        report_parts.append(f"Holat: {self.topshiriq.get_status_display()}")
        
        if self.topshiriq.tugash_vaqti:
            report_parts.append(f"Muddat: {self.topshiriq.tugash_vaqti.strftime('%Y-%m-%d %H:%M')}")
            
        report_parts.append(f"\nTopshiriq matni:\n{self.topshiriq.body}")
        
        # Javob ma'lumotlari
        if self.javob:
            report_parts.append("\n=== JAVOB MA'LUMOTLARI ===")
            if self.javob.title:
                report_parts.append(f"Javob sarlavhasi: {self.javob.title}")
            report_parts.append(f"Javob matni:\n{self.javob.body}")
            if self.javob.izoh:
                report_parts.append(f"Izoh:\n{self.javob.izoh}")
                
        # Fayllar ma'lumotlari
        topshiriq_files = self.topshiriq.files.all()
        if topshiriq_files:
            report_parts.append("\n=== TOPSHIRIQ FAYLLARI ===")
            for file in topshiriq_files:
                report_parts.append(f"- {file.file.name}")
                
        if self.javob:
            javob_files = self.javob.files.all()
            if javob_files:
                report_parts.append("\n=== JAVOB FAYLLARI ===")
                for file in javob_files:
                    report_parts.append(f"- {file.file.name}")
        
        # Statistika
        report_parts.append(f"\n=== STATISTIKA ===")
        if self.duration_days:
            report_parts.append(f"Bajarilish muddati: {self.duration_days} kun")
        report_parts.append(f"Hisobot yaratilgan: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        self.full_report = "\n".join(report_parts)
        return self.full_report
        self.full_report = "\n".join(report_parts)
        return self.full_report

