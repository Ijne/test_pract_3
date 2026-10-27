import unittest
from decimal import Decimal

from budget_planner import BudgetPlanner


class BudgetPlannerTDDTests(unittest.TestCase):
    def test_new_planner_has_zero_balance(self):
        planner = BudgetPlanner()
        self.assertEqual(planner.remaining, Decimal("0.00"))

    def test_setting_budget_changes_remaining_amount(self):
        planner = BudgetPlanner()
        planner.set_budget("50000")
        self.assertEqual(planner.remaining, Decimal("50000.00"))

    def test_expense_reduces_remaining_amount(self):
        planner = BudgetPlanner("10000")
        planner.add_expense("Продукты", "1250.50")
        self.assertEqual(planner.remaining, Decimal("8749.50"))

    def test_multiple_expenses_are_summed(self):
        planner = BudgetPlanner("10000")
        planner.add_expense("Транспорт", "500")
        planner.add_expense("Продукты", "1200")
        self.assertEqual(planner.total_expenses, Decimal("1700.00"))

    def test_invalid_amounts_are_rejected(self):
        planner = BudgetPlanner("1000")
        for amount in ("0", "-1", "abc"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    planner.add_expense("Ошибка", amount)

    def test_report_contains_totals_and_categories(self):
        planner = BudgetPlanner("5000")
        planner.add_expense("Продукты", "1200")
        planner.add_expense("Транспорт", "300")
        report = planner.generate_report()
        self.assertEqual(report["budget"], Decimal("5000.00"))
        self.assertEqual(report["expenses"], Decimal("1500.00"))
        self.assertEqual(report["remaining"], Decimal("3500.00"))
        self.assertEqual(report["by_category"]["Продукты"], Decimal("1200.00"))


if __name__ == "__main__":
    unittest.main()
