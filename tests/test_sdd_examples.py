import csv
import unittest
from decimal import Decimal
from pathlib import Path

from budget_planner import BudgetPlanner


class SpecificationByExampleTests(unittest.TestCase):
    def test_examples_from_specification_table(self):
        table = Path(__file__).parents[1] / "specifications" / "budget_examples.csv"
        with table.open(encoding="utf-8", newline="") as source:
            examples = list(csv.DictReader(source))
        self.assertGreater(len(examples), 0)
        for row in examples:
            with self.subTest(case=row["case"]):
                planner = BudgetPlanner(row["budget"])
                planner.add_expense(row["category"], row["expense"])
                report = planner.generate_report()
                self.assertEqual(report["expenses"], Decimal(row["expected_total_expenses"]).quantize(Decimal("0.01")))
                self.assertEqual(report["remaining"], Decimal(row["expected_remaining"]).quantize(Decimal("0.01")))
                self.assertEqual(report["overspent"], row["overspent"].lower() == "true")


if __name__ == "__main__":
    unittest.main()
