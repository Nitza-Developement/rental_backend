# Generated by Django 5.0.2 on 2024-06-01 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0036_alter_vehicle_make_alter_vehicle_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='odometer',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]