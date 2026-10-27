import unittest
from decimal import Decimal

from budget_planner import BudgetPlanner


class BudgetPlannerAcceptanceTests(unittest.TestCase):
    def test_user_sets_budget_and_registers_two_expenses(self):
        planner = BudgetPlanner()
        planner.set_budget("60000")
        planner.add_expense("Жильё", "25000")
        planner.add_expense("Продукты", "8500")
        self.assertEqual(planner.total_expenses, Decimal("33500.00"))
        self.assertEqual(planner.remaining, Decimal("26500.00"))

    def test_report_reflects_overspending(self):
        planner = BudgetPlanner("5000")
        planner.add_expense("Ремонт", "6200")
        report = planner.generate_report()
        self.assertEqual(report["remaining"], Decimal("-1200.00"))
        self.assertTrue(report["overspent"])


if __name__ == "__main__":
    unittest.main()
