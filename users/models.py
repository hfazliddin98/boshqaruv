import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.choices import UserRoleChoice


class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)

    class Meta:
        abstract = True


class Bolim(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Users(AbstractUser):
    sharif = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=UserRoleChoice.choices)
    bolim = models.ForeignKey(Bolim, on_delete=models.CASCADE, blank=True, null=True)
    bolim_boshligi = models.BooleanField(default=False)
    parol = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username