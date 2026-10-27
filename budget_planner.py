"""Предметная модель планировщика бюджета для варианта 61."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


MONEY = Decimal("0.01")


def _money(value, *, allow_zero=False):
    """Преобразовать значение в денежную сумму с точностью до копеек."""
    try:
        amount = Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Сумма должна быть числом") from exc
    if amount < 0 or (amount == 0 and not allow_zero):
        raise ValueError("Сумма должна быть положительной")
    return amount


@dataclass(frozen=True)
class Expense:
    category: str
    amount: Decimal


class BudgetPlanner:
    """Устанавливает бюджет, учитывает расходы и формирует сводный отчёт."""

    def __init__(self, budget=0):
        self._budget = _money(budget, allow_zero=True)
        self._expenses = []

    @property
    def budget(self):
        return self._budget

    @property
    def total_expenses(self):
        return sum((item.amount for item in self._expenses), Decimal("0.00"))

    @property
    def remaining(self):
        return (self.budget - self.total_expenses).quantize(MONEY)

    def set_budget(self, amount):
        self._budget = _money(amount)

    def add_expense(self, category, amount):
        normalized_category = str(category).strip()
        if not normalized_category:
            raise ValueError("Категория расхода не может быть пустой")
        expense = Expense(normalized_category, _money(amount))
        self._expenses.append(expense)
        return expense

    def generate_report(self):
        by_category = {}
        for expense in self._expenses:
            by_category[expense.category] = (
                by_category.get(expense.category, Decimal("0.00")) + expense.amount
            ).quantize(MONEY)
        return {
            "budget": self.budget,
            "expenses": self.total_expenses,
            "remaining": self.remaining,
            "overspent": self.remaining < 0,
            "by_category": by_category,
        }
