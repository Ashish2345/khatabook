from django.urls import path

from .views import ExpenseListView

app_name = "expenses"

urlpatterns = [path("expense-list/", ExpenseListView.as_view(), name="expense-list")]
