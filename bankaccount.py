class BankAccount():

    def __init__(self):  
        '''Constructor to set account_number to '0', pin_number to an empty string,
           balance to 0.0, interest_rate to 0.0 and transaction_list to an empty list.'''              
        self.account_number = '0'
        self.pin_number = ''
        self.balance = 0.0
        self.interest_rate = 0.0
        self.transaction_list = []
        

    def deposit_funds(self, amount):
        '''Function to deposit an amount to the account balance. Raises an
           exception if it receives a value that cannot be cast to float.'''
        try:
            amount_to_deposit = float(amount)
            self.balance = float(self.balance) + amount_to_deposit            
            transaction = ('Deposit',amount_to_deposit)
            self.transaction_list.append(transaction)
            #print(self.balance)            
        except Exception as error:
            print(repr(error))
            
        

    def withdraw_funds(self, amount):
        '''Function to withdraw an amount from the account balance. Raises an
           exception if it receives a value that cannot be cast to float. Raises
           an exception if the amount to withdraw is greater than the available
           funds in the account.'''
        try:
            amount_to_withdraw = float(amount)
            if(amount_to_withdraw > self.balance):
                raise Exception('Withdrawal amount exceeds available funds.')
            self.balance = float(self.balance) - amount_to_withdraw            
            transaction = ('Withdrawal',amount_to_withdraw)
            self.transaction_list.append(transaction)
            #print(self.balance)            
        except Exception as error:
            print(repr(error))
        
        
    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or "Withdrawal" on
           the first line, and then the amount deposited or withdrawn on the next line.'''        
        #transaction = self.transaction_list[-1]
        transaction = self.transaction_list
        transaction_string = ''        
        for index, t in enumerate(self.transaction_list):
            transaction_string = transaction_string + str(t[0])+'\n'+str(t[1])+'\n'            
        return transaction_string
        


    def save_to_file(self):
        '''Function to overwrite the account text file with the current account
           details. Account number, pin number, balance and interest (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''        
        account_num = self.account_number
        filename = account_num.strip() + '.txt'
        f = open(filename, 'w')
        f.write(str(self.account_number).strip())
        f.write("\n")
        f.write(str(self.pin_number).strip())
        f.write("\n")
        f.write(str(self.balance).strip())
        f.write("\n")
        f.write(str(self.interest_rate).strip())
        f.write("\n")
        transaction_string = self.get_transaction_string()
        #print(transaction_string)
        f.write(transaction_string)
        f.close()
