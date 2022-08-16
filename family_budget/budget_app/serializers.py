from rest_framework import serializers
from .models import Budget, BudgetRecord


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetRecord
        fields = '__all__'
