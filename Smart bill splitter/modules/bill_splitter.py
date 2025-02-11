class BillSplitter:
    def __init__(self):
        self.balances={}
    def add_expense(self,expense):#updates each person’s balance (who owes how much).
        payer= expense.payer #get the person who paid. For example: Alice pays for the entire meal $30
        split_amount=expense.split_amount() #calculate how much each participant should pay. Each participant owes #10

        if payer not in self.balances: #Update payer's balance (Alice gets credited)
            self.balances[payer]=0
        self.balances[payer]+=expense.amount #Alice: +30

        for person in expense.participants: #update participants balances
            if person not in self.balances:
                self.balances[person] = 0
            self.balances[person]-=split_amount #Bob:-10, Charlie:-10

    def settle_expense(self):
        """
        Finds the minimum transactions required to settle debts.
        Updates `self.balances` so that payments are reflected.
        Allows multiple participants to contribute towards the remaining debt.
        """
        creditors = []  # People who are owed money
        debtors = []  # People who owe money
        # Categorize people as creditors (+ balance) or debtors (- balance)
        for person, balance in self.balances.items():
            if balance > 0:
                creditors.append((person, balance))  # Creditors (owed money)
            elif balance < 0:
                debtors.append((person, -balance))  # Debtors (owe money)
        if not creditors or not debtors:
            print("No debts to settle.")
            return []
        transactions = []  # Store the list of transactions
        tolerance = 0.01  # Small floating-point precision allowance
        while True:
            debt_remaining = sum(balance for _, balance in debtors)
            if debt_remaining <= tolerance:
                print("\nAll debts have been settled! ✅")
                break
            for i, (debtor, debt_amount) in enumerate(debtors[:]):  # Loop through debtors
                if debt_amount <= tolerance:
                    continue  # Skip fully settled debtors

                for j, (creditor, credit_amount) in enumerate(creditors[:]):  # Loop through creditors
                    if credit_amount <= tolerance:
                        continue  # Skip fully settled creditors

                    print(f"\n{debtor} initially owed {creditor} ${debt_amount:.2f}")

                    # Get the payment amount
                    payment = float(input(f"{debtor}, how much can you pay now? (Max: ${debt_amount:.2f}): "))

                    # Ensure payment is valid (allowing small floating-point tolerance)
                    while payment <= 0 or payment > debt_amount + tolerance:
                        print("Invalid amount. Please enter a valid amount.")
                        payment = float(input(f"{debtor}, how much can you pay now? (Max: ${debt_amount:.2f}): "))

                    transactions.append(f"{debtor} pays {creditor} ${payment:.2f}")

                    # ✅ Update balances in self.balances
                    self.balances[debtor] += payment  # Reduce debtor's balance (closer to zero)
                    self.balances[creditor] -= payment  # Reduce creditor's balance (closer to zero)

                    new_debt_amount = debt_amount - payment  # Reduce debtor's debt
                    new_credit_amount = credit_amount - payment  # Reduce creditor's credit

                    # Update or remove debtor
                    if new_debt_amount > tolerance:
                        debtors[i] = (debtor, new_debt_amount)  # Update debtor's balance
                    else:
                        debtors.pop(i)  # ✅ Remove debtor when fully paid
                        continue  # Skip further processing

                    # Update or remove creditor
                    if new_credit_amount > tolerance:
                        creditors[j] = (creditor, new_credit_amount)  # Update creditor's balance
                    else:
                        creditors.pop(j)  # ✅ Remove creditor when fully repaid
                        continue  # Skip further processing

            # **New Feature: Ask If Someone Wants to Pay More**
            print("\nCurrent debt status:")
            for debtor, amount in debtors:
                print(f"{debtor} still owes ${amount:.2f}")

            # Ask if anyone wants to contribute more
            extra_payment = input("\nDoes anyone want to contribute more towards clearing the debt? (yes/no): ").strip().lower()
            if extra_payment != "yes":
                break  # Stop additional payments if no one wants to contribute

        return transactions  # Return the list of transactions
