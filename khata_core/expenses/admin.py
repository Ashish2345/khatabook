from django.contrib import admin

from .models import Expense, ExpenseCategory, PaymentMethod, RecurringExpense


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "payment_method", "amount", "date")
    list_filter = ("category", "payment_method", "date", "user")
    search_fields = ("description",)


@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "category",
        "payment_method",
        "amount",
        "start_date",
        "end_date",
        "frequency",
    )
    list_filter = ("category", "payment_method", "frequency", "start_date", "user")
    search_fields = ("description",)
