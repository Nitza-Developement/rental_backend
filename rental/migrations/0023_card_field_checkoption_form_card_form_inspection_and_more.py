# Generated by Django 5.0.2 on 2024-05-11 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0022_alter_client_options_alter_contract_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('required', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('TEXT', 'Text'), ('NUMBER', 'Number'), ('SINGLE_CHECK', 'Single Check'), ('IMAGE', 'Image'), ('SIGNATURE', 'Signature'), ('EMAIL', 'Email'), ('PHONE', 'Phone'), ('DATE', 'Date'), ('TIME', 'Time')], max_length=20)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='rental.card')),
            ],
        ),
        migrations.CreateModel(
            name='CheckOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_options', to='rental.field')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forms', to='rental.tenant')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.form'),
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='rental.form')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='rental.tenant')),
                ('tenantUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='rental.tenantuser')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspections', to='rental.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='FieldResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('checked', models.BooleanField(blank=True, null=True)),
                ('check_option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response', to='rental.checkoption')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_response', to='rental.field')),
                ('tenantUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_responses', to='rental.tenantuser')),
                ('inspection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_responses', to='rental.inspection')),
            ],
        ),
    ]
