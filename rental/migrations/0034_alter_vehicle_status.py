# Generated by Django 5.0.2 on 2024-05-29 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0033_vehicle_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Unavailable', 'Unavailable'), ('Rented', 'Rented'), ('In Maintenance', 'In Maintenance')]),
        ),
    ]
