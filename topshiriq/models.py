from django.db import models
from topshiriq.choices import StatusChoice
from users.models import AsosiyModel, Users


class RektorTopishiriq(AsosiyModel):
    rektor_user = models.ForeignKey(Users, on_delete=models.PROTECT)
    prorektor_user = models.ForeignKey(Users, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    izoh = models.TextField(blank=True)

class RektorTopishiriqFile(models.Model):
    rektor_topishiriq = models.ForeignKey(RektorTopishiriq, on_delete=models.CASCADE, related_name='rektor_topishiriq_files')
    file = models.FileField(upload_to='rektor_topishiriq_files/')

    def __str__(self):
        return self.file.name