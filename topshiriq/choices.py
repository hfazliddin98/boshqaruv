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


# Map user roles to unified task type
ROLE_TO_TOPSHIRIQ_TYPE = {
    RoleChoice.REKTOR: TopshiriqType.REKTOR,
    RoleChoice.PROREKTOR: TopshiriqType.PROREKTOR,
    RoleChoice.BOLIM_BOSHLIGI: TopshiriqType.BOLIM_BOSHLIGI,
    RoleChoice.DEKAN: TopshiriqType.DEKAN,
    RoleChoice.ZAM_DEKAN: TopshiriqType.ZAMDEKAN,
    RoleChoice.KAFEDRA_MUDIRI: TopshiriqType.KAFEDRA_MUDIRI,
    RoleChoice.TYUTOR: TopshiriqType.TUTOR,
    RoleChoice.HODIM: TopshiriqType.XODIM,
    # No direct match; use a sensible default
    RoleChoice.KOMISSIYA: TopshiriqType.XODIM,
}