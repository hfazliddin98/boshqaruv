from django.db import models


class RoleChoice(models.TextChoices):
    ADMIN = ("Admin", "Admin")
    REKTOR = ("Rektor", "Rektor")
    PROREKTOR = ("Prorektor", "Prorektor")
    DEKAN = ("Dekan", "Dekan")
    BOLIM_RAHBARI = ("Bo'lim rahbari", "Bo'lim rahbari")
    BOLIM_BOSHLIGI = ("Bo'lim boshligi", "Bo'lim boshligi")
    ZAM_DEKAN = ("Zam dekan", "Zam dekan")
    KAFEDRA_MUDIRI = ("Kafedra mudiri", "Kafedra mudiri")
    TYUTOR = ("Tyutor", "Tyutor")
    HODIM = ("Hodim", "Hodim")
    KOMISSIYA = ("Komissiya", "Komissiya")


ALLOWED_USER_MAP = {
    RoleChoice.ADMIN: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}


class TopshiriqJavobStatus(models.TextChoices):
    JARAYONDA = ("Jarayonda", "Jarayonda")
    BAJARILDI = ("Bajarildi", "Bajarildi")
    QISMAN_BAJARILDI = ("Qisman bajarildi", "Qisman bajarildi")
    KECHIKTIRILDI = ("Kechiktirildi", "Kechiktirildi")
    BEKOR_QILINDI = ("Bekor qilindi", "Bekor qilindi")
    QAYTA_ISHLASH = ("Qayta ishlash", "Qayta ishlash")


# Kimga topshiriq javob berish huquqi bor
ALLOWED_JAVOB_MAP = {
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
    RoleChoice.TYUTOR: [RoleChoice.HODIM],
}

# Kimga javob ko'rish huquqi bor (yuqori lavozimlar pastki lavozimlar javoblarini ko'ra oladi)
ALLOWED_VIEW_JAVOB_MAP = {
    RoleChoice.ADMIN: [RoleChoice.REKTOR, RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM, RoleChoice.KOMISSIYA],
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR, RoleChoice.DEKAN, RoleChoice.BOLIM_RAHBARI, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN, RoleChoice.BOLIM_BOSHLIGI, RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI, RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN, RoleChoice.TYUTOR, RoleChoice.HODIM],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR, RoleChoice.HODIM],
}
