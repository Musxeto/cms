# Generated by Django 5.0.8 on 2024-08-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0011_department_alter_employee_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_hr_manager',
            field=models.BooleanField(default=False),
        ),
    ]
