import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "name", "amount", "category"])


def read_expenses():
    initialize_file()
    rows = []
    with open(FILENAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            r["amount"] = float(r["amount"]) if r.get("amount") else 0.0
            rows.append(r)
    return rows


def add_expense_row(name, amount, category, date=None):
    initialize_file()
    date = date or datetime.now().strftime("%Y-%m-%d")
    with open(FILENAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, name, amount, category])


def totals_by_category(expenses):
    totals = {}
    for e in expenses:
        cat = e.get("category", "Unsorted") or "Unsorted"
        totals[cat] = totals.get(cat, 0.0) + float(e.get("amount", 0))
    return totals


def monthly_total(expenses, year_month):
    total = 0.0
    for e in expenses:
        if e.get("date", "").startswith(year_month):
            total += float(e.get("amount", 0))
    return total
