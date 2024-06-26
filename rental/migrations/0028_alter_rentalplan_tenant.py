# Generated by Django 5.0.2 on 2024-05-19 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0027_alter_rentalplan_tenant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rentalplan",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="plans",
                to="rental.tenant",
            ),
        ),
    ]
