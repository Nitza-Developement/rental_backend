# Generated by Django 5.0.2 on 2024-07-31 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0047_contractform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractform',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='rental.contractformtemplate'),
        ),
        migrations.CreateModel(
            name='ContractFormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeholder', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('TEXT', 'Text'), ('NUMBER', 'Number'), ('SIGNATURE', 'Signature'), ('EMAIL', 'Email'), ('PHONE', 'Phone')], max_length=20)),
                ('required', models.BooleanField(default=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='rental.contractformtemplate')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rental.tenantuser')),
            ],
        ),
    ]
