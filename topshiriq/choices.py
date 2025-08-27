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






ALLOWED_TOPSHIRIQ_MAP = {
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}


# Kimga javoblarni ko'rish huquqi bor (yuqori lavozimlar pastki lavozimlar javoblarini ko'ra oladi)
ALLOWED_TOPSHIRIQ_VIEW_MAP = {
    RoleChoice.KOMISSIYA: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.ADMIN: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.REKTOR, RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}

ALLOWED_TOPSHIRIQ_JAVOB_MAP = {
    RoleChoice.PROREKTOR: [RoleChoice.REKTOR],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.PROREKTOR],
    RoleChoice.DEKAN: [RoleChoice.PROREKTOR],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.BOLIM_RAHBARI],
    RoleChoice.HODIM: [RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.DEKAN],
    RoleChoice.ZAM_DEKAN: [RoleChoice.DEKAN],
    RoleChoice.TYUTOR: [RoleChoice.ZAM_DEKAN],
}

# Kimga javoblarni ko'rish huquqi bor (yuqori lavozimlar pastki lavozimlar javoblarini ko'ra oladi)
ALLOWED_TOPSHIRIQ_JAVOB_VIEW_MAP = {
    RoleChoice.KOMISSIYA: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.ADMIN: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.REKTOR, RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}
