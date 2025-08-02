import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from users.choices import RoleChoice


class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Bolim(AsosiyModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    sharif = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=30, choices=RoleChoice.choices, default=RoleChoice.HODIM)
    bolim = models.ForeignKey(Bolim, on_delete=models.PROTECT, blank=True, null=True)
    parol = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
    
