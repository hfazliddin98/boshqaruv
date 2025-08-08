from django.db import models
from users.models import AsosiyModel, Users
from topshiriq.choices import TopshiriqType
from prorektor.choices import StatusChoice, XolatChoice



class Topshiriq(AsosiyModel):
    topshiriq_type = models.CharField(max_length=50, choices=TopshiriqType.choices)  # Qaysi roldagi topshiriq
    yaratuvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='yaratuvchi_user_topshiriqlar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='bajaruvchi_user_topshiriqlar')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=XolatChoice.choices, default=XolatChoice.ODDIY)
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    javob_yuborildi = models.BooleanField(default=False)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Topshiriq #{self.pk}"

    class Meta:
        indexes = [
            models.Index(fields=['topshiriq_type']),                # Rol bo‘yicha tez topish
            models.Index(fields=['yaratuvchi_user']),          # Yaratgan user bo‘yicha
            models.Index(fields=['bajaruvchi_user']),          # Bajaruvchi bo‘yicha
            models.Index(fields=['status']),                   # Holat bo‘yicha
            models.Index(fields=['javob_yuborildi']),                   # Javob yuborilganligi bo‘yicha
            models.Index(fields=['boshlanish_vaqti']),          # Sana bo‘yicha
            models.Index(fields=['topshiriq_type', 'status']),      # Rol + holat kombinatsiyasi
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

    