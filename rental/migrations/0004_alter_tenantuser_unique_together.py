# Generated by Django 5.0.2 on 2024-04-28 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0003_remove_user_is_staff'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tenantuser',
            unique_together={('user', 'is_default')},
        ),
    ]
