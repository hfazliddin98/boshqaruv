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


class TopshiriqType(models.TextChoices):
    REKTOR = "rektor", "Rektor"
    PROREKTOR = "prorektor", "Prorektor"
    BOLIM_RAHBARI = "bolim_rahbari", "Bo'lim rahbari"
    BOLIM_BOSHLIGI = "bolim_boshligi", "Bo'lim boshligi"
    DEKAN = "dekan", "Dekan"
    ZAMDEKAN = "zamdekan", "Zamdekan"
    KAFEDRA_MUDIRI = "kafedra_mudiri", "Kafedra mudiri"
    TUTOR = "tyutor", "Tyutor"
    XODIM = "xodim", "Xodim"