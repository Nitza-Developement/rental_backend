# Generated by Django 5.0.2 on 2024-06-24 14:09

import rental.notes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0042_alter_inspection_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldresponse',
            name='checked',
        ),
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=rental.notes.models.get_file_path),
        ),
    ]