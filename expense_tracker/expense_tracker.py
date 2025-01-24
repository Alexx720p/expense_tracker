import datetime
import argparse
from utils import ExpenseTracker


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
    delete_parser.add_argument('id', type=str, help='id of the expense to delete')

    update_parser = subparsers.add_parser('update', help='Update an existing expense')
    update_parser.add_argument('id', type=str, help='id of the expense to update')
    update_parser.add_argument('new_description', type=str, help='New description for the expense')
    update_parser.add_argument('new_amount', type=float, help='New amount for the expense')
    update_parser.add_argument('new_date', type=str, help='New date for the expense in YYYY-MM-DD format')

    export_parser = subparsers.add_parser('export', help='Export expenses to a CSV file')
    export_parser.add_argument('filename', type=str, help='Filename for the exported CSV')

    summary_parser = subparsers.add_parser('summary', help='Show a summary of expenses')
    summary_parser.add_argument('--year', type=int, help='Year for the summary')
    summary_parser.add_argument('--month', type=int, help='Month for the summary')
    summary_parser.add_argument('--category', type=str, help='Category for the summary')


    budget_parser = subparsers.add_parser('set_budget', help='Show the budget')
    budget_parser.add_argument('amount', type=float, help='Amount of the budget')

    subparsers.add_parser('check_budget', help='Check the budget')

    subparsers.add_parser('clear', help='Clear the list of expenses')


    args = parser.parse_args()
    tracker = ExpenseTracker()

    if args.command == 'add':
        date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None
        tracker.add_expense(args.description, args.amount, args.category, date )

    elif args.command == 'view':
        tracker.view_expenses(args.category)

    elif args.command == 'delete':
        tracker.delete_expense(args.id)

    elif args.command == 'update':
        tracker.update_expense(args.id, args.new_description, args.new_amount, args.new_date)

    elif args.command == 'summary':
        tracker.summary(args.year, args.month, args.category)

    elif args.command == 'export':
        tracker.export_to_csv(args.filename)

    elif args.command == 'set_budget':
        tracker.set_budget(args.amount)

    elif args.command == 'check_budget':
        tracker.check_budget()

    elif args.command == 'clear':
        tracker.clear_list()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()