from django.db.models import fields
from rest_framework import serializers
from .models import Expense 

class ExpenseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Expense 
        feilds = ("user","expense_name","name","transaction_date","category")