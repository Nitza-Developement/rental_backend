# Generated by Django 5.0.2 on 2024-05-02 13:58

import rental.vehicle.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0016_alter_vehicle_tenant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclepicture',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehiclepicture',
            name='image',
            field=models.ImageField(upload_to=rental.vehicle.models.get_image_path),
        ),
    ]