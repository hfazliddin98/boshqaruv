from django.db import models


class StatusChoice(models.TextChoices):
    ADMIN = ('admin', 'admin')
    PROREKTOR = ('prorektor', 'prorektor')
    RAHBAR = ('rahbar', 'rahbar')
    HODIM = ('hodim', 'hodim')

class XolatChoice(models.TextChoices):
    BAJARILDI = ('Bajarildi', 'Bajarildi')
    BAJARILMADI = ('Bajarilmadi', 'Bajarilmadi')
    KECHIKDI = ('Kechikdi', 'Kechikdi')