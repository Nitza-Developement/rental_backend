# Generated by Django 5.0.2 on 2024-04-29 00:27

import rental.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0009_alter_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, validators=[rental.user.models.user_name_validator]),
        ),
    ]
