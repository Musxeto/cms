# Generated by Django 5.0.8 on 2024-08-20 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0034_alter_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='experience',
            field=models.TextField(blank=True),
        ),
    ]