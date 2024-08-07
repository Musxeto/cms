from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone',
            'address',
            'date_of_birth',
            'department',
            'position',
            'profile_image'
        ]