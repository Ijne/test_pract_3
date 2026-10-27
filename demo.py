from budget_planner import BudgetPlanner


def main():
    planner = BudgetPlanner("50000")
    planner.add_expense("Продукты", "8250.40")
    planner.add_expense("Транспорт", "2100")
    planner.add_expense("Связь", "750")
    report = planner.generate_report()
    print(f"Бюджет: {report['budget']:.2f} руб.")
    print(f"Расходы: {report['expenses']:.2f} руб.")
    print(f"Остаток: {report['remaining']:.2f} руб.")
    for category, amount in report["by_category"].items():
        print(f"  {category}: {amount:.2f} руб.")


if __name__ == "__main__":
    main()
