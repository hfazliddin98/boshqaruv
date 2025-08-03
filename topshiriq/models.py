from django.db import models
from topshiriq.choices import StatusChoice, XolatChoice
from users.models import AsosiyModel, Users


class RektorTopshiriq(AsosiyModel):
    yaratuvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='yaratgan_topshiriqlar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='bajaruvchi_topshiriqlar')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=XolatChoice.choices, default=XolatChoice.ODDIY)
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Topshiriq #{self.pk}"

class RektorTopshiriqFile(models.Model):
    rektor_topshiriq = models.ForeignKey(RektorTopshiriq, on_delete=models.CASCADE, related_name='rektor_topshiriq_files')
    file = models.FileField(upload_to='rektor_topshiriq_files/')

    def __str__(self):
        return self.file.name


class RektorTopshiriqJavob(models.Model):
    rektor_topshiriq = models.ForeignKey(RektorTopshiriq, on_delete=models.CASCADE, related_name='rektor_topshiriq_javob_files')
    sender = models.ForeignKey(Users, on_delete=models.PROTECT)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Javob #{self.pk} - {self.rektor_topshiriq.title}"
    

class RektorTopshiriqJavobFile(models.Model):
    rektor_topshiriq_javob = models.ForeignKey(RektorTopshiriqJavob, on_delete=models.CASCADE, related_name='rektor_topshiriq_javob_files')
    file = models.FileField(upload_to='rektor_topshiriq_javob_files/')

    def __str__(self):
        return self.file.name