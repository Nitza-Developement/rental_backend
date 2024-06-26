# Generated by Django 5.0.2 on 2024-05-03 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0020_alter_stageupdate_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tracker",
            options={
                "ordering": ["created_date"],
                "verbose_name": "Tracker",
                "verbose_name_plural": "Trackers",
            },
        ),
        migrations.AlterModelOptions(
            name="trackerheartbeatdata",
            options={
                "ordering": ["-timestamp"],
                "verbose_name": "Tracker Heart Beat Data",
                "verbose_name_plural": "Tracker Heart Beat Data",
            },
        ),
        migrations.AlterField(
            model_name="tracker",
            name="vehicle",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracker",
                to="rental.vehicle",
            ),
        ),
    ]
