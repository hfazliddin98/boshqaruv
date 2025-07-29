from django.db import models
from users.models import AsosiyModel


class RektorToposhiriq(AsosiyModel):
    title = models.CharField(max_length=255, blank=True)