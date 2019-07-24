from rest_framework import serializers
from emp.models import User, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['emp_id', 'address', 'gender', 'mgr_id']
        depth=1


class UserSerializer(serializers.ModelSerializer):
    emp = EmployeeSerializer(source='employee_set', many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'phone', 'role', 'emp']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'phone', 'role', 'emp']
        extra_kwargs = {'password': {'write_only': True}}
