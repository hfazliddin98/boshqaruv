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
    RoleChoice.REKTOR: [RoleChoice.PROREKTOR],
    RoleChoice.PROREKTOR: [RoleChoice.BOLIM_RAHBARI, RoleChoice.DEKAN],
    RoleChoice.BOLIM_RAHBARI: [RoleChoice.BOLIM_BOSHLIGI],
    RoleChoice.BOLIM_BOSHLIGI: [RoleChoice.HODIM],
    RoleChoice.DEKAN: [RoleChoice.KAFEDRA_MUDIRI, RoleChoice.ZAM_DEKAN],
    RoleChoice.KAFEDRA_MUDIRI: [RoleChoice.HODIM],
    RoleChoice.ZAM_DEKAN: [RoleChoice.TYUTOR],
}
