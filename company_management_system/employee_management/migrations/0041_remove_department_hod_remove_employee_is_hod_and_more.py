# Generated by Django 5.0.8 on 2024-08-23 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0040_remove_department_manager_department_hod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='HOD',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_hod',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='is_manager',
        ),
        migrations.AddField(
            model_name='department',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_departments', to=settings.AUTH_USER_MODEL),
        ),
    ]