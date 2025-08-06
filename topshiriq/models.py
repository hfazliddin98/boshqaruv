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


class RektorTopshiriqFile(AsosiyModel):
    rektor_topshiriq = models.ForeignKey(RektorTopshiriq, on_delete=models.CASCADE, related_name='rektor_topshiriq_files')
    file = models.FileField(upload_to='rektor_topshiriq_files/')

    def __str__(self):
        return self.file.name


class RektorTopshiriqJavob(AsosiyModel):
    rektor_topshiriq = models.ForeignKey(RektorTopshiriq, on_delete=models.CASCADE, related_name='rektor_topshiriq_javob_files')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT)  
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    izoh = models.TextField(blank=True)
    
    def __str__(self):
        return f"Javob #{self.pk} - {self.title or self.rektor_topshiriq.title}"
    

class RektorTopshiriqJavobFile(AsosiyModel):
    rektor_topshiriq_javob = models.ForeignKey(RektorTopshiriqJavob, on_delete=models.CASCADE, related_name='rektor_topshiriq_javob_files')
    file = models.FileField(upload_to='rektor_topshiriq_javob_files/')

    def __str__(self):
        return self.file.name
    


class ProrektorBolimTopshiriq(AsosiyModel):
    yaratuvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='prorektor_bolim_yaratgan_topshiriqlar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='prorektor_bolim_bajaruvchi_topshiriqlar')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=XolatChoice.choices, default=XolatChoice.ODDIY)
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Bo'lim topshiriq #{self.pk}"


class ProrektorBolimTopshiriqFile(AsosiyModel):
    prorektor_bolim_topshiriq = models.ForeignKey(ProrektorBolimTopshiriq, on_delete=models.CASCADE, related_name='prorektor_bolim_topshiriq_files')
    file = models.FileField(upload_to='prorektor_bolim_topshiriq_files/')

    def __str__(self):
        return self.file.name


class ProrektorBolimTopshiriqJavob(AsosiyModel):
    prorektor_bolim_topshiriq = models.ForeignKey(ProrektorBolimTopshiriq, on_delete=models.CASCADE, related_name='prorektor_bolim_topshiriq_javob_files')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return f"Javob #{self.pk} - {self.title or self.prorektor_bolim_topshiriq.title}"


class ProrektorBolimTopshiriqJavobFile(AsosiyModel):
    prorektor_bolim_topshiriq_javob = models.ForeignKey(ProrektorBolimTopshiriqJavob, on_delete=models.CASCADE, related_name='prorektor_bolim_topshiriq_javob_files')
    file = models.FileField(upload_to='prorektor_bolim_topshiriq_javob_files/')

    def __str__(self):
        return self.file.name



class ProrektorDekanTopshiriq(AsosiyModel):
    yaratuvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='prorektor_dekan_yaratgan_topshiriqlar')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT, related_name='prorektor_dekan_bajaruvchi_topshiriqlar')
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=StatusChoice.choices, default=StatusChoice.YUBORILDI)
    xolat = models.CharField(max_length=30, choices=XolatChoice.choices, default=XolatChoice.ODDIY)
    boshlanish_vaqti = models.DateTimeField(null=True, blank=True)
    tugash_vaqti = models.DateTimeField(null=True, blank=True)
    bajarilgan_vaqti = models.DateTimeField(null=True, blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Dekan topshiriq #{self.pk}"


class ProrektorDekanTopshiriqFile(AsosiyModel):
    prorektor_dekan_topshiriq = models.ForeignKey(ProrektorDekanTopshiriq, on_delete=models.CASCADE, related_name='prorektor_dekan_topshiriq_files')
    file = models.FileField(upload_to='prorektor_dekan_topshiriq_files/')

    def __str__(self):
        return self.file.name


class ProrektorDekanTopshiriqJavob(AsosiyModel):
    prorektor_dekan_topshiriq = models.ForeignKey(ProrektorDekanTopshiriq, on_delete=models.CASCADE, related_name='prorektor_dekan_topshiriq_javob_files')
    bajaruvchi_user = models.ForeignKey(Users, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    izoh = models.TextField(blank=True)

    def __str__(self):
        return f"Javob #{self.pk} - {self.title or self.prorektor_dekan_topshiriq.title}"


class ProrektorDekanTopshiriqJavobFile(AsosiyModel):
    prorektor_dekan_topshiriq_javob = models.ForeignKey(ProrektorDekanTopshiriqJavob, on_delete=models.CASCADE, related_name='prorektor_dekan_topshiriq_javob_files')
    file = models.FileField(upload_to='prorektor_dekan_topshiriq_javob_files/')

    def __str__(self):
        return self.file.name