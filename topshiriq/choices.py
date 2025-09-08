from django.db import models

from users.choices import RoleChoice


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
    KOMISSIYA = "komissiya", "Komissiya"



ALLOWED_TOPSHIRIQ_MAP = {
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.BOLIM_HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.KAFEDRA_HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}


ALLOWED_TOPSHIRIQ_JAVOB_MAP = {
    RoleChoice.PROREKTOR: [RoleChoice.REKTOR],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.PROREKTOR],
    RoleChoice.DEKAN: [RoleChoice.PROREKTOR],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.BOLIM_RAHBARI],
    RoleChoice.BOLIM_HODIM: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.DEKAN],
    RoleChoice.KAFEDRA_HODIM: [RoleChoice.KAFEDRA_MUDIRI],
    RoleChoice.ZAM_DEKAN: [RoleChoice.DEKAN],
    RoleChoice.TYUTOR: [RoleChoice.ZAM_DEKAN],
}
