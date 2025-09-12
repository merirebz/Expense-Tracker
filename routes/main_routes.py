from flask import Blueprint, request, redirect, url_for, render_template, send_file
from utils.expense_utils import (
    read_expenses,
    add_expense_row,
    totals_by_category,
    monthly_total,
)

from datetime import datetime

main_routes = Blueprint("main_routes", __name__)


@main_routes.route("/", methods=["GET"])
def index():
    expenses = read_expenses()

    selected_month = request.args.get("month")
    monthly = None

    if selected_month:
        try:
            datetime.strptime(selected_month + "-01", "%Y-%m-%d")
            monthly = monthly_total(expenses, selected_month)
        except:
            monthly = 0.0

    totals = totals_by_category(expenses)
    expenses_sorted = sorted(expenses, key=lambda x: x.get("date", ""), reverse=True)

    return render_template(
        "index.html",
        expenses=expenses_sorted,
        totals=totals,
        monthly=monthly,
        selected_month=selected_month,
    )


@main_routes.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    amount = request.form.get("amount")
    category = request.form.get("category")

    try:
        amt = float(amount)
    except:
        amt = 0.0

    add_expense_row(name, amt, category)
    return redirect(url_for("main_routes.index"))


@main_routes.route("/download")
def download():
    return send_file("expenses.csv", as_attachment=True)
