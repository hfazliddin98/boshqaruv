import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from users.choices import RoleChoice


class AsosiyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    


class Struktura(AsosiyModel):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=RoleChoice.choices, default=RoleChoice.BOLIM_HODIM)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Struktura'
        verbose_name_plural = 'Strukturalar'
        ordering = ['role']



class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sharif = models.CharField(max_length=255, blank=True)
    struktura = models.ForeignKey(Struktura, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.CharField(max_length=30, choices=RoleChoice.choices, default=RoleChoice.BOLIM_HODIM)
    yaratgan_user = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users',
        verbose_name='Yaratgan foydalanuvchi'
    )
    parol = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
    

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
            models.Index(fields=['date_joined']),
            models.Index(fields=['username']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['struktura', 'role']),
        ]

