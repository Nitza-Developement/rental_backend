# Generated by Django 5.0.2 on 2024-05-16 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0024_alter_field_type_alter_fieldresponse_note"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="tenantuser",
            unique_together=set(),
        ),
    ]
