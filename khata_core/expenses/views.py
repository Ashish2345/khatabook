from django.views.generic import ListView
from django.db.models import Max, Min, Sum

from .models import Expense


class ExpenseListView(ListView):
    model = Expense
    template_name = "expenses/expenses_list.html"
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_expenses = Expense.objects.aggregate(total_expenses=Sum("amount"))[
            "total_expenses"
        ]
        top_stats = Expense.objects.annotate(
            max_spent=Max("amount"), min_spent=Min("amount")
        )
        context["total_expenses"] = total_expenses
        context["top_stats"] = top_stats
        return context
