from django.db import models 
from django.utils import timezone
from account.models import Accountdb


# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(Accountdb, on_delete=models.CASCADE)  # ForeignKey to the User model
    expense_name = models.CharField(max_length=255, help_text="Expense name/description")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount spent")
    transaction_date = models.DateField(default=timezone.now, help_text="Date of transaction")
    
    # Define choices for the category field
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
        # Add more categories as needed
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, help_text="Category of expense")

    def __str__(self):
        return self.expense_name 
    
    