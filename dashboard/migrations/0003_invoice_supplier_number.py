# Generated by Django 5.0.2 on 2024-03-01 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_company_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='supplier_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
