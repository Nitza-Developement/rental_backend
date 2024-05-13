from django.db import models
from rental.models import Tenant, TenantUser, Vehicle


class Form(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="forms")


class Inspection(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="inspections")
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="inspections"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="inspections"
    )
    tenantUser = models.ForeignKey(
        TenantUser, on_delete=models.CASCADE, related_name="inspections"
    )
    created_at = models.DateTimeField(auto_now=True)


class Card(models.Model):
    name = models.CharField(max_length=255)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)


class Field(models.Model):

    TEXT = "Text"
    NUMBER = "Number"
    SINGLE_CHECK = "Single Check"
    IMAGE = "Image"
    SIGNATURE = "Signature"
    EMAIL = "Email"
    PHONE = "Phone"
    DATE = "Date"
    TIME = "Time"

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


class CheckOption(models.Model):
    name = models.CharField(max_length=255, blank=True)
    field = models.ForeignKey(
        Field, on_delete=models.CASCADE, related_name="check_options"
    )


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
        CheckOption, on_delete=models.SET_NULL, null=True, related_name="response"
    )
    inspection = models.ForeignKey(
        Inspection, on_delete=models.CASCADE, null=True, related_name="field_responses"
    )