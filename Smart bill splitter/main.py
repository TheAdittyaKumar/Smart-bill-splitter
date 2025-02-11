import sys
import os

# Ensure Python can find the "modules" folder
sys.path.append(os.path.abspath("modules"))

# Import required classes
from bill_splitter import BillSplitter
from expense import Expense
from file_handler import FileHandler

def main():
    splitter = BillSplitter()
    expenses = FileHandler.load_expenses()

    # Ensure loaded expenses update balances
    for expense in expenses:
        splitter.add_expense(expense)

    while True:
        print("\nSmart Bill Splitter")
        print("1. Add an expense")
        print("2. Show balances")
        print("3. Settle debts")
        print("4. Save & Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            # Get basic expense details
            payer = input("Enter payer's name: ").strip()
            amount = float(input("Enter amount: ").strip())

            # Ask if the payer is included in the split
            while True:
                include_payer = input("Is the bill going to be split by everyone including the person you owe money? (yes/no): ").strip().lower()
                if include_payer in ["yes", "no"]:
                    break
                print("Invalid input. Please enter 'yes' or 'no'.")

            # Get participants
            participants = input("Enter participants (comma-separated): ").strip().split(",")
            participants = [p.strip() for p in participants]

            # If the payer should be included, ensure they are in the list
            if include_payer == "yes" and payer not in participants:
                participants.append(payer)

            # If the payer should NOT be included, remove them from the list
            if include_payer == "no" and payer in participants:
                participants.remove(payer)

            # Create an expense and add it to the system
            expense = Expense(payer, amount, participants)
            splitter.add_expense(expense)
            expenses.append(expense)
            print("✅ Expense added!")

        elif choice == "2":
            print("\n📊 Current Balances:")
            for person, balance in splitter.balances.items():
                print(f"{person}: ${balance:.2f}")

        elif choice == "3":
            transactions = splitter.settle_expense()  # ✅ Fix: Method name corrected
            print("\n💰 Settlement Transactions:")
            for transaction in transactions:
                print(transaction)

        elif choice == "4":
            transactions = splitter.settle_expense()  # ✅ Ensure transactions are settled before saving
            FileHandler.save_expenses(expenses, transactions)  # ✅ Fix: Save transactions too
            print("💾 Data saved successfully. Exiting...")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
