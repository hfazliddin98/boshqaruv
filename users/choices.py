from django.db import models


class RoleChoice(models.TextChoices):
    ADMIN = ('admin', 'admin')
    REKTOR = ('Rektor', 'Rektor')
    PROREKTOR = ('Prorektor', 'Prorektor')
    DEKAN = ('Dekan', 'Dekan')
    BOLIM_BOSHLIGI = ('Bo\'lim boshligi', 'Bo\'lim boshligi')
    ZAM_DEKAN = ('Zam dekan', 'Zam dekan')
    KAFEDRA_MUDIRI = ('Kafedra mudiri', 'Kafedra mudiri')
    TYUTOR = ('Tyutor', 'Tyutor')
    HODIM = ('Hodim', 'Hodim')
    KOMISSIYA = ('Komissiya', 'Komissiya')