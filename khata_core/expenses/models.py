from django.db import models
from general.models import AuditFields


class ExpenseCategory(AuditFields):
    """
    Model to represent different expense categories.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Expense Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PaymentMethod(AuditFields):
    """
    Model to represent different payment methods.
    """

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Payment Methods"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Expense(AuditFields):
    """
    Model to represent an expense entry.
    """

    category = models.ForeignKey(
        ExpenseCategory, on_delete=models.SET_NULL, null=True, related_name="expenses"
    )
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True, related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to="receipts/", blank=True, null=True)

    class Meta:
        ordering = ["-date", "-created_date"]

    def __str__(self):
        return (
            f"{self.amount} - {self.category.name if self.category else 'No Category'}"
        )


class RecurringExpense(AuditFields):
    """
    Model to represent recurring expenses.
    """

    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recurring_expenses",
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recurring_expenses",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    frequency = models.CharField(
        max_length=50,
        choices=[
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.amount} - {self.category.name if self.category else 'No Category'} (Recurring)"
