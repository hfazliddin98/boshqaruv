from django.db import models


class UserRoleChoice(models.TextChoices):
    SUPERADMIN = ('superadmin', 'superadmin')
    ADMIN = ('admin', 'admin')
    HODIM = ('hodim', 'hodim')