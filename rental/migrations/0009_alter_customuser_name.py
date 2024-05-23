# Generated by Django 5.0.2 on 2024-04-29 00:26

import rental.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0008_customuser_name_alter_customuser_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(
                default=None,
                max_length=100,
                validators=[rental.user.models.user_name_validator],
            ),
        ),
    ]
