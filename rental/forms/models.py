from django.db import models
from rental.models import Tenant, TenantUser


class Form(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="forms")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=255)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="cards")

    def __str__(self) -> str:
        return self.name


class Field(models.Model):

    TEXT = "TEXT"
    NUMBER = "NUMBER"
    SINGLE_CHECK = "SINGLE_CHECK"
    IMAGE = "IMAGE"
    SIGNATURE = "SIGNATURE"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    DATE = "DATE"
    TIME = "TIME"

    FORM_FIELD_TYPES = (
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (SINGLE_CHECK, "Single Check"),
        (IMAGE, "Image"),
        (SIGNATURE, "Signature"),
        (EMAIL, "Email"),
        (PHONE, "Phone"),
        (DATE, "Date"),
        (TIME, "Time"),
    )

    name = models.CharField(max_length=255)
    required = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=FORM_FIELD_TYPES)
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, null=True, related_name="fields"
    )

    def __str__(self) -> str:
        return self.name


class CheckOption(models.Model):

    DEFAULT = "DEFAULT"
    POINT_PASS = "POINT_PASS"
    POINT_FAIL = "POINT_FAIL"

    CHECKOPTION_TYPES = (
        (DEFAULT, "default"),
        (POINT_PASS, "Point pass"),
        (POINT_FAIL, "Point fail"),
    )

    name = models.CharField(max_length=255, blank=True)
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="check_options"
    )
    type = models.CharField(max_length=20, choices=CHECKOPTION_TYPES, default="DEFAULT")

    def __str__(self) -> str:
        return self.name


class FieldResponse(models.Model):
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, null=True)
    checked = models.BooleanField(blank=True, null=True)
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="field_response"
    )
    tenantUser = models.ForeignKey(
        TenantUser, on_delete=models.CASCADE, related_name="field_responses"
    )
    check_option = models.ForeignKey(
        CheckOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="response",
    )
    inspection = models.ForeignKey(
        "Inspection",
        on_delete=models.CASCADE,
        null=True,
        related_name="field_responses",
    )

    def __str__(self) -> str:
        return str(self.inspection)
