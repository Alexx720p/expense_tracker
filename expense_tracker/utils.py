import datetime
import csv
import os
import json
from rich import print
from rich.console import Console
from rich.table import Table
from rich import box

class ExpenseTracker:
    def __init__(self, storage_file='expenses.csv'):
        self.expenses = []
        self.storage_file = storage_file
        self.budget = None
        self.console=Console()
        self.load_data()

    def add_expense(self, description, amount, category, date=None):
        expense_id = len(self.expenses) + 1
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("Amount cannot be negative.")
        
            if date is None:
                date = datetime.date.today()
            expense = {
                'id': expense_id,
                'description': description,
                'amount': amount,
                'category': category,
                'date': date
            }
        
            self.expenses.append(expense)
            self.save_data()
            self.console.print(f"[bold green]Added expense: {description}, Amount: {amount}, Category: {category}, Date: {date}[/bold green]")
    
        except ValueError as e:
            self.console.print(f"[bold red]Error: {e}[/bold red]")

    def view_expenses(self, category=None):
        if not self.expenses:
            self.console.print("[bold red]No expenses recorded.[/bold red]")
            return
        table=Table(title="Expenses",box=box.ROUNDED)
        table.add_column("ID",style="blue", no_wrap=True)
        table.add_column("Description",style="cyan", no_wrap=True)
        table.add_column("Amount",style="magenta")
        table.add_column("Category",style="green")
        table.add_column("Date",style="yellow")
        if category is None:
            for expense in self.expenses:
                table.add_row(expense['id'],expense['description'],str(expense['amount']),expense['category'], str(expense['date']))
        else:
            filtered_expenses = [expense for expense in self.expenses if expense['category'] == category]
            if filtered_expenses:
                self.console.print(f"[bold green]Expenses for category '{category}':[/bold green]")
                for expense in filtered_expenses:
                    table.add_row(expense['id'], expense['description'],str(expense['amount']),expense['category'], str(expense['date']))
            else:
                self.console.print(f"[bold red]No expenses found for category '{category}'.[/bold red]")
        self.console.print(table)

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense['id'] == expense_id:
                self.expenses.remove(expense)
                self.reassign_ids(self.expenses)
                self.save_data()
                self.console.print(f"[bold green]Deleted expense with id: {expense_id}[/bold green]")
                return
        print(f"[bold red]Expense with id '{expense_id}' not found.[/bold red]")

    def update_expense(self, expense_id, new_description=None, new_amount=None, new_date=None):
        for expense in self.expenses:
            if expense['id'] == expense_id:
                if new_description is not None:
                    expense['description'] = new_description
                if new_amount is not None:
                    expense['amount'] = new_amount
                if new_date is not None:
                    expense['date'] = new_date
                self.save_data()
                print(f"[bold green]Updated expense with ID {expense_id}[/bold green]")
                return
        self.console.print(f"[bold red]Expense with ID '{expense_id}' not found.[/bold red]")

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

    def set_budget(self, amount):
        self.budget = float(amount)
        self.console.print(f"[bold green]Budget set to: {self.budget:.2f}[/bold green]")
        self.save_budget()

    def check_budget(self):
        self.load_budget()
        if self.budget is None:
            self.console.print("[bold red]Budget not set.[/bold red]")
        else:
            self.console.print(f"[bold green]Budget: {self.budget:.2f}[/bold green]")
            total = self.get_total_expenses()
            if total > self.budget:
                print(f"[bold red]Total expenses: {total:.2f}, over budget by {total - self.budget:.2f}[/bold red]")
            else:
                print(f"[bold green]Total expenses: {total:.2f}, under budget by {self.budget - total:.2f}[/bold green]")

    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'description', 'amount', 'category', 'date'])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)
        print(f"[bold green]Expenses exported to {filename}[/bold green]")

    def clear_list(self):
        self.expenses = []
        self.save_data()
        self.console.print("[bold green]List of expenses cleared.[/bold green]")

    def save_budget(self):
        with open('budget.json', 'w') as file:
            json.dump(self.budget, file)

    def load_budget(self):
        if os.path.exists('budget.json'):
            with open('budget.json', 'r') as file:
                self.budget = json.load(file)

    def get_total_expenses(self):
        return sum([float(expense['amount']) for expense in self.expenses])

    def save_data(self):
        with open(self.storage_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'description', 'amount', 'category', 'date' ])
            writer.writeheader()
            for expense in self.expenses:
                writer.writerow(expense)

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                self.expenses = [row for row in reader]

    def reassign_ids(self, expenses):
        '''Reassign IDs to tasks to ensure they are sequential'''
        for index, self.expense in enumerate(expenses):
            self.expense['id'] = index + 1