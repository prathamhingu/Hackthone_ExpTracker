from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    EXPENSE_CATEGORIES = (
        ('groceries', 'Groceries'),
        ('rent', 'Rent'),
        ('salary', 'Salary'),
        ('tip', 'Tip'),
        ('food', 'Food'),
        ('medical', 'Medical'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('transportation', 'Transportation'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(
        max_length=20,
        choices=EXPENSE_CATEGORIES,
        blank=True,  # Allow blank for income transactions
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)  # Optional description
    date = models.DateField()

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} ({self.user.username})"

    def save(self, *args, **kwargs):
        if self.transaction_type == 'income':
            self.category = ''  # Ensure no category for income transactions
        super().save(*args, **kwargs)
