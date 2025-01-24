#expense_tracker

https://roadmap.sh/projects/expense-tracker


How to use it:
-Clone/copy this repo in your environment and write the following commands:


Commands:


-add expense: python expense_tracker.py add '(expense description)' (expense amount) (expense category) (expense date (YYYY-MM-DD))

$ python expense_tracker.py add 'Phone Bill' 35 Utilities 2025-01-07


-view all expenses: python expense_tracker.py view 

$ python expense_tracker.py view


-view expenses for a specific category: python expense_tracker.py view --category (category you want to filter by)

$ python expense_tracker.py view --category Utilities


-delete an expense: python expense_tracker.py delete (expense id)

$ python expense_tracker.py delete 9


-update an expense: python expense_tracker.py update (id of the expense you want to update)(new description)(new amount)(new date)

$ python expense_tracker.py update 8 Books 39 2025-06-20


-summary (all expenses): python expense_tracker.py summary

$ python expense_tracker.py summary


-summary (for a specific month ): python expense_tracker.py summary --year YYYY --month MM

$ python expense_tracker.py summary --year 2025 --month 01


-summary (for a specific category): python expense_tracker.py summary --category (category)

$ python expense_tracker.py summary --category Utilities


-setting a budget: python expense_tracker.py set_budget (amount of the budget)

$ python expense_tracker.py set_budget 500


-check budget: python expense_tracker.py check_budget

$ python expense_tracker.py check_budget


-exporting expenses list: python expense_tracker.py export (file name)

$ python expense_tracker.py export 'expenses jan 2025'


-clearing the expenses list: python expense_tracker.py clear

$ python expense_tracker.py clear


Note: you may need to install the rich library
