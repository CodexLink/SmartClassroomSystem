from django.db import models
from .admintypes import AdminDeclaredTypes
from django.core.validators import MinValueValidator, MaxValueValidator

# ! User Type is Admin, therefore requires less information than Staff / Teachers.


class AdminDataSet(models.Model):
    ads_FN = models.CharField(
        max_length=20,
        null=False,
        blank=False)

    ads_MN = models.CharField(
        max_length=20,
        null=True,
        blank=True)

    ads_LN = models.CharField(
        max_length=50,
        null=False,
        blank=False)

    ads_AN = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(
            18), MaxValueValidator(75)])

    ads_UserP = models.CharField(
        max_length=20,
        null=False,
        blank=False)

    ads_PassP = models.CharField(
        max_length=64,
        null=False,
        blank=False)

    ads_UserFP = models.CharField(
        max_length=255,
        null=False,
        blank=False)  # Unconfirmed

    ads_RoleT = models.CharField(
        max_length=30,
        choices=AdminDeclaredTypes,
        default=AdminDeclaredTypes[0])

    def __str__(self):
        # To be sterilized
        return self.ads_FirstName
