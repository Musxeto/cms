# Generated by Django 5.0.8 on 2024-08-15 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0013_compliancereport_employeerecord_jobposting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
