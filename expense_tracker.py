import datetime
import argparse
import csv
import os
import json

class ExpenseTracker:
    def __init__(self, storage_file='expenses.csv'):
        self.expenses = []
        self.storage_file = storage_file
        self.budget = None
        self.load_data()

    def set_budget(self, amount):
        self.budget = float(amount)
        print(f"Budget set to {amount:.2f}")
        self.save_budget()

    def save_budget(self):
        with open('budget.json', 'w') as file:
            json.dump(self.budget, file)

    def load_budget(self):
        if os.path.exists('budget.json'):
            with open('budget.json', 'r') as file:
                self.budget = json.load(file)

    def check_budget(self):
        self.load_budget()
        if self.budget is None:
            print("Budget not set.")
        
        else:
            print(f"Budget: {self.budget:.2f}")
            total = self.get_total_expenses()
            if total > self.budget:
                print(f"Total expenses: {total:.2f}, over budget by {total - self.budget:.2f}")
            else:
                print(f"Total expenses: {total:.2f}, under budget by {self.budget - total:.2f}")
        
    
    def add_expense(self, description, amount, category, date=None):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount cannot be negative.")
        
            if date is None:
                date = datetime.date.today()
        
            expense = {
                'description': description,
                'amount': amount,
                'category': category,
                'date': date
            }
        
            self.expenses.append(expense)
            self.save_data()
            print(f"Added expense: {description}, Amount: {amount}, Category: {category}, Date: {date}")
    
        except ValueError as e:
            print(f"Error: {e}")

    def get_total_expenses(self):
        return sum([float(expense['amount']) for expense in self.expenses])

    def view_expenses(self, category=None):
        if not self.expenses:
            print("No expenses recorded.")
            return
        if category is None:
            for expense in self.expenses:
                print(f"Description: {expense['description']}, Amount: {expense['amount']}, Category: {expense['category']}, Date: {expense['date']}")
        else:
            filtered_expenses = [expense for expense in self.expenses if expense['category'] == category]
            if filtered_expenses:
                print(f"Expenses for category '{category}':")
                for expense in filtered_expenses:
                    print(f"Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}")
            else:
                print(f"No expenses found for category '{category}'.")

    def delete_expense(self, description):
        for expense in self.expenses:
            if expense['description'] == description:
                self.expenses.remove(expense)
                self.save_data()
                print(f"Deleted expense: {description}")
                return
        print(f"Expense with description '{description}' not found.")

    def update_expense(self, description, new_description=None, new_amount=None, new_date=None):
        for expense in self.expenses:
            if expense['description'] == description:
                if new_description is not None:
                    expense['description'] = new_description
                if new_amount is not None:
                    expense['amount'] = new_amount
                if new_date is not None:
                    expense['date'] = new_date
                self.save_data()
                print(f"Updated expense: {expense}")
                return

    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['description', 'amount', 'category', 'date'])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)
        print(f"Expenses exported to {filename}")

    def save_data(self):
        with open(self.storage_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['description', 'amount', 'category', 'date' ])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]

    def summary(self, year=None, month=None):
        if year is not None and month is not None:
            # Filter expenses for the specified month and year
            filtered_expenses = [
                expense for expense in self.expenses
                if datetime.datetime.strptime(expense['date'], '%Y-%m-%d').year == year and
                    datetime.datetime.strptime(expense['date'], '%Y-%m-%d').month == month
            ]
            summary_type = f"for {year}-{month:02d}"
        else:
            # Use all expenses if no specific month and year are provided
            filtered_expenses = self.expenses
            summary_type = "for all time"

        # Calculate the total amount for the filtered expenses
        total_amount = sum(float(expense['amount']) for expense in filtered_expenses)
        total_expenses = len(filtered_expenses)
        
        # Print the summary
        print(f"Summary {summary_type}:")
        print(f"Total expenses: {total_expenses}")
        print(f"Total amount spent: {total_amount:.2f}")



def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('description', type=str, help='Description of the expense')
    add_parser.add_argument('amount', type=float, help='Amount of the expense')
    add_parser.add_argument('category', type=str, help='Category of the expense')
    add_parser.add_argument('date', type=str, nargs='?', help='Date of the expense in YYYY-MM-DD format')

    view_parser = subparsers.add_parser('view', help='View all expenses')
    view_parser.add_argument('--category', type=str, help='Filter expenses by category')

    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('description', type=str, help='Description of the expense to delete')

    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('description', type=str, help='Description of the expense to update')
    update_parser.add_argument('--new_description', type=str, help='New description for the expense')
    update_parser.add_argument('--new_amount', type=float, help='New amount for the expense')
    update_parser.add_argument('--new_date', type=str, help='New date for the expense in YYYY-MM-DD format')

    export_parser = subparsers.add_parser('export', help='Export expenses to a CSV file')
    export_parser.add_argument('filename', type=str, help='Filename for the exported CSV')

    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    summary_parser.add_argument('--year', type=int, help='Year for the summary')
    summary_parser.add_argument('--month', type=int, help='Month for the summary')

    budget_parser = subparsers.add_parser('set_budget', help='Show the budget')
    budget_parser.add_argument('amount', type=float, help='Amount of the budget')

    subparsers.add_parser('check_budget', help='Check the budget')


    args = parser.parse_args()
    tracker = ExpenseTracker()

    if args.command == 'add':
        date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None
        tracker.add_expense(args.description, args.amount, args.category, date )

    elif args.command == 'view':
        tracker.view_expenses(args.category)

    elif args.command == 'delete':
        tracker.delete_expense(args.description)

    elif args.command == 'update':
        tracker.update_expense(args.description, args.new_description, args.new_amount, args.new_date)

    elif args.command == 'summary':
        tracker.summary(args.year, args.month)

    elif args.command == 'export':
        tracker.export_to_csv(args.filename)

    elif args.command == 'set_budget':
        tracker.set_budget(args.amount)

    elif args.command == 'check_budget':
        tracker.check_budget()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()