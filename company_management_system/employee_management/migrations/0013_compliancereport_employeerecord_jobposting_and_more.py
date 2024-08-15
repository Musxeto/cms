# Generated by Django 5.0.8 on 2024-08-15 05:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0012_employee_is_hr_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplianceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=255)),
                ('generated_on', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='compliance_reports/')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(max_length=100)),
                ('job_history', models.TextField(blank=True)),
                ('current_salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('benefits', models.TextField(blank=True)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='employee_management.department')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_name', models.CharField(max_length=255)),
                ('applicant_email', models.EmailField(max_length=254)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('cover_letter', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('job_posting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='employee_management.jobposting')),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_type', models.CharField(max_length=100)),
                ('reason', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.TextField(blank=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payrolls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateField()),
                ('comments', models.TextField()),
                ('rating', models.IntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reviews', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
