from django.db import models


class XolatChoice(models.TextChoices):
    SHOSHILINCH = ('Shoshilinch', 'Shoshilinch')
    ORTA = ('O`rta', 'O`rta')
    ODDIY = ('Oddiy', 'Oddiy')


class StatusChoice(models.TextChoices):
    YUBORILDI = ('Yuborildi', 'Yuborildi')
    BAJARILDI = ('Bajarildi', 'Bajarildi')
    BAJARILMADI = ('Bajarilmadi', 'Bajarilmadi')
    KECHIKDI = ('Kechikdi', 'Kechikdi')