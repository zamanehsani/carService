# Generated by Django 5.0.2 on 2024-03-01 10:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_invoice_supplier_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.company'),
        ),
    ]
