# Generated by Django 5.0.2 on 2024-02-28 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_alter_battery_customer_alter_battery_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.company'),
        ),
    ]
