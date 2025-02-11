import csv
from modules.expense import Expense

class FileHandler:
    @staticmethod
    def load_expenses(filename="data/expenses.csv"):
        """Loads expenses from a CSV file."""
        expenses = []
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                first_row = next(reader, None)  # Read the first row safely

                # Check if the file is empty
                if first_row is None:
                    print("Warning: expenses.csv is empty. No data loaded.")
                    return expenses  # Return empty list

                for row in reader:
                    if len(row) < 3:
                        continue  # Skip invalid rows
                    payer, amount, participants = row
                    expenses.append(Expense(payer, float(amount), participants.split(",")))
                    
        except FileNotFoundError:
            print("Warning: expenses.csv not found. Creating a new file on exit.")
        except Exception as e:
            print(f"Error loading expenses: {e}")

        return expenses

    @staticmethod
    def save_expenses(expenses, transactions, expense_filename="data/expenses.csv", transaction_filename="data/transactions.csv"):
        """Saves expenses and transactions to separate CSV files."""
        try:
            # Save expenses
            with open(expense_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Payer", "Amount", "Participants"])  # Header
                for expense in expenses:
                    writer.writerow([expense.payer, expense.amount, ",".join(expense.participants)])

            # Save transactions separately
            with open(transaction_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["From", "To", "Amount"])  # Header
                for transaction in transactions:
                    parts = transaction.split()
                    writer.writerow([parts[0], parts[2], parts[4]])  # Extract names and amount

            print("✅ Expenses and transactions successfully saved!")
        except Exception as e:
            print(f"⚠️ Error saving data: {e}")
