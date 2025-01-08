import datetime
import argparse
import csv
import os

class ExpenseTracker:
    def __init__(self, storage_file='expenses.csv'):
        self.expenses = []
        self.storage_file = storage_file
        self.load_expenses()

    def add_expense(self, description, amount, date=None):
        if date is None:
            date = datetime.date.today()
        expense = {
            'description': description,
            'amount': amount,
            'date': date
        }
        self.expenses.append(expense)
        self.save_expenses()
        print(f"Added expense: {description}, Amount: {amount}, Date: {date}")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
            return
        for expense in self.expenses:
            print(f"Description: {expense['description']}, Amount: {expense['amount']}, Date: {expense['date']}")

    def delete_expense(self, description):
        for expense in self.expenses:
            if expense['description'] == description:
                self.expenses.remove(expense)
                print(f"Deleted expense: {description}")
                return
        print(f"Expense with description '{description}' not found.")

    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['description', 'amount', 'date'])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)
        print(f"Expenses exported to {filename}")

    def save_expenses(self):
        with open(self.storage_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['description', 'amount', 'date'])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)

    def load_expenses(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]



def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add expense command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('description', type=str, help='Description of the expense')
    add_parser.add_argument('amount', type=float, help='Amount of the expense')
    add_parser.add_argument('--date', type=str, help='Date of the expense in YYYY-MM-DD format', default=None)

    # View expenses command
    subparsers.add_parser('view', help='View all expenses')

    # Delete expense command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('description', type=str, help='Description of the expense to delete')

    args = parser.parse_args()
    tracker = ExpenseTracker()

    if args.command == 'add':
        date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None
        tracker.add_expense(args.description, args.amount, date)
    elif args.command == 'view':
        tracker.view_expenses()
    elif args.command == 'delete':
        tracker.delete_expense(args.description)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()