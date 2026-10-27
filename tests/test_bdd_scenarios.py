import re
import unittest
from decimal import Decimal
from pathlib import Path

from budget_planner import BudgetPlanner


class GherkinScenarioRunnerTests(unittest.TestCase):
    def test_all_feature_scenarios(self):
        feature = Path(__file__).parents[1] / "features" / "budget.feature"
        text = feature.read_text(encoding="utf-8")
        scenarios = re.findall(
            r"Сценарий: (.+?)\n\s+Допустим бюджет установлен в размере ([\d.-]+) рублей"
            r"\n\s+Когда я регистрирую расход ([\d.-]+) рублей в категории \"(.+?)\""
            r"\n\s+Тогда оставшаяся сумма равна ([\d.-]+) рублей",
            text,
        )
        self.assertGreater(len(scenarios), 0)
        for name, budget, expense, category, expected in scenarios:
            with self.subTest(scenario=name):
                planner = BudgetPlanner(budget)
                planner.add_expense(category, expense)
                self.assertEqual(planner.remaining, Decimal(expected).quantize(Decimal("0.01")))


if __name__ == "__main__":
    unittest.main()
