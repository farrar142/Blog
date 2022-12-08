from django.db import models


class PermissionType(models.IntegerChoices):
    FREE_TO_USE = 0
    LOGIN_REQUIRED = 1
    OWNER_OWNED = 2
