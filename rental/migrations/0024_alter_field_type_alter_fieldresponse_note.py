# Generated by Django 5.0.2 on 2024-05-11 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rental", "0023_card_field_checkoption_form_card_form_inspection_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="field",
            name="type",
            field=models.CharField(
                choices=[
                    ("Text", "Text"),
                    ("Number", "Number"),
                    ("Single Check", "Single Check"),
                    ("Image", "Image"),
                    ("Signature", "Signature"),
                    ("Email", "Email"),
                    ("Phone", "Phone"),
                    ("Date", "Date"),
                    ("Time", "Time"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="fieldresponse",
            name="note",
            field=models.TextField(blank=True, null=True),
        ),
    ]
