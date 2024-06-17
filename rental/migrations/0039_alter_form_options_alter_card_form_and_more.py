# Generated by Django 5.0.2 on 2024-06-09 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0038_alter_vehicle_spare_tires"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="form",
            options={"ordering": ["created_at"]},
        ),
        migrations.AlterField(
            model_name="card",
            name="form",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cards",
                to="rental.form",
            ),
        ),
        migrations.AlterField(
            model_name="fieldresponse",
            name="check_option",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="response",
                to="rental.checkoption",
            ),
        ),
    ]
