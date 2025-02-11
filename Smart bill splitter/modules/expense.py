class Expense:
    def __init__(self,payer,amount,participants):
        self.payer=payer
        self.amount=amount
        self.participants=participants
    def split_amount(self):
        return self.amount/len(self.participants)
    
        