# models/expense.py
class Expense:
    def __init__(self, name, amount, category, date):
        self.name = name
        self.amount = float(amount)
        self.category = category
        self.date = date
