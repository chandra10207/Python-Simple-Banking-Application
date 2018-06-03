import tkinter as tk
import os 
from tkinter import messagebox
from tkinter import *
from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from bankaccount import BankAccount

win = tk.Tk()
# Set window size here to '440x640' pixels
win.geometry('440x640')
# Set window title here to 'FedUni Banking'
win.winfo_toplevel().title("FedUni Banking")

# The account number entry and associated variable
account_number_var = tk.StringVar()
account_number_entry = tk.Entry(win, textvariable=account_number_var)
account_number_entry.focus_set()

# The pin number entry and associated variable.
# Note: Modify this to 'show' PIN numbers as asterisks (i.e. **** not 1234)
pin_number_var = tk.StringVar()
account_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var)

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('Balance: $0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_entry = tk.Entry(win)

# The transaction text widget holds text of the accounts transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The bank account object we will work with
account = BankAccount()

# ---------- Button Handlers for Login Screen ----------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    pin_number_var.set('')

def handle_pin_button(event):      
    '''Function to add the number of the button clicked to the PIN number entry via its associated variable.'''
    account_pin_entry.focus_set()
    current_btn_value = event.widget["text"]
    Current_pin_var = pin_number_var.get()
    final_pin_var = Current_pin_var + current_btn_value
    # Limit to 4 chars in length
    if(len(final_pin_var) > 4):
        messagebox.showerror('Pin Error','Pin Number must be of 4 character')
    else:
        # Set the new pin number on the pin_number_var
        pin_number_var.set(final_pin_var)
    

def log_in(event):
    '''Function to log in to the banking system using a known account number and PIN.'''
    global account
    global pin_number_var
    global account_num_entry
    global account_file

    # Create the filename from the entered account number with '.txt' on the end
    account_num = account_number_var.get()
    filename = account_num + '.txt'
    filepath = os.path.isfile('./'+filename)
    #print(filepath)
    
    # Try to open the account file for reading    
    try:
        # Open the account file for reading
        account_file = open(filename, "r")
        # First line is account number
        account_number   = account_file.readline()
        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
        account_pin      = account_file.readline()
        # Read third and fourth lines (balance and interest rate)        
        account_balance  = account_file.readline()
        account_interest = account_file.readline()
        
        if( int(account_pin.strip()) != int(pin_number_var.get())):
            raise Exception("Incorrect Pin Number")
        transaction_list = []
        # Section to read account transactions from file - start an infinite 'do-while' loop here
        while True:
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list 
            line = account_file.readline()
            if not line:
                #print('End of file!')
                break
            amount = account_file.readline()
            transaction = (line.strip(),amount.strip())
            transaction_list.append(transaction)  
        # Close the file now we're finished with it
        account_file.close()
        #account = BankAccount(account_number,account_pin,account_)        
        account.account_number = account_number
        account.pin_number = account_pin
        account.balance = account_balance
        account.interest_rate = account_interest
        account.transaction_list = transaction_list
        
        # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen    
        remove_all_widgets()
        create_account_screen()  
    # Catch exception if we couldn't open the file or PIN entered did not match account PIN      
    except Exception as error:
        print(repr(error))
        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror('Login failed','"Bad account number or pin.')
        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        account_number_entry.focus_set()
        

    
    

# ---------- Button Handlers for Account Screen ----------

def save_and_log_out():
        
    '''Function  to overwrite the account file with the current state of
       the account object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global account

    # Save the account with any new transactions
    #print(account)
    account.save_to_file()
    
    # Reset the bank acount object
    account = BankAccount()

    # Reset the account number and pin to blank
    account.account_number = ''
    account.pin_number = ''
    

    # Remove all widgets and display the login screen again    
    remove_all_widgets()
    create_login_screen()
    

def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       account's transaction list.'''
    global account,account_file    
    global amount_entry
    global amount_entry_var
    global balance_label
    global balance_var,transaction_text_widget,transaction_text_widget_var

    try:       

        # Try to increase the account balance and append the deposit to the account file
        new_entry = amount_entry_var.get()        
        balance = account.balance
        total_balance = float(new_entry) + float(balance)
        account_num = account.account_number
        filename = account_num.strip() + '.txt'
        #print(filename)
        f = open(filename, 'a')
        f.write("\n")
        f.write('Deposit')
        f.write("\n")
        print(new_entry)
        f.write(new_entry)
        #data = f.readlines()
        f.close()
        #print(account_file)
        #account_file.writeline('Deposit')

        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        cash_amount = new_entry

        # Deposit funds
        account.deposit_funds(cash_amount)    
            
        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.

        transaction_string = account.get_transaction_string()        
        transaction_text_widget.config(state='normal')        
        transaction_text_widget.delete(1.0,END)
        transaction_text_widget.insert(INSERT, str(transaction_string))            
        transaction_text_widget.config(state='disabled') 
        

        # Change the balance label to reflect the new balance    
        balance_var.set('Balance: $'+str(total_balance))
        
        # Clear the amount entry
        amount_entry_var.set('')   
        

        # Update the interest graph with our new balance
        plot_interest_graph()

    except Exception as error:
        print(repr(error))
        #messagebox.showerror('Transaction Error',repr(error))
        messagebox.showerror('Transaction Error','Illegal numerical value.')

    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
        
def perform_withdrawal():
    '''Function to withdraw the amount in the amount entry from the account balance and add an entry to the transaction list.'''
     
    global account
    global amount_entry
    global amount_entry_var
    global balance_label
    global balance_var
    global transaction_text_widget

    # Try to increase the account balance and append the deposit to the account file
    try:
        new_entry = amount_entry_var.get()        
        balance = account.balance
        amount_to_withdraw = float(new_entry)
        total_amount = float(balance)
        if(amount_to_withdraw <= total_amount):            
            total_balance = total_amount - amount_to_withdraw
            account_num = account.account_number
            filename = account_num.strip() + '.txt'
            #print(filename)
            f = open(filename, 'a')
            f.write("\n")
            f.write('Withdraw')
            f.write("\n")
            #print(new_entry)
            f.write(new_entry)
            #data = f.readlines()
            f.close()    
            # Get the cash amount to deposit. Note: We check legality inside account's withdraw_funds method        
            cash_amount = amount_to_withdraw
        
            # Withdraw funds        
            account.withdraw_funds(cash_amount) 
        

            # Update the transaction widget with the new transaction by calling account.get_transaction_string()
            # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
            #       contents, and finally configure back to state='disabled' so it cannot be user edited.        

            transaction_string = account.get_transaction_string()        
            transaction_text_widget.config(state='normal')
            transaction_text_widget.delete(1.0,END)
            transaction_text_widget.insert(INSERT, str(transaction_string))            
            transaction_text_widget.config(state='disabled')        

            # Change the balance label to reflect the new balance           
            balance_var.set('Balance: $'+str(total_balance))

            # Clear the amount entry
            amount_entry_var.set('') 

            # Update the interest graph with our new balance
            plot_interest_graph()
        else:
            messagebox.showerror('Transaction Error','Withdrawal amount exceeds available funds.')

    # Catch and display any returned exception as a messagebox 'showerror'
    except Exception as error:
        print(repr(error))
        messagebox.showerror('Transaction Error','Illegal numerical value.')
        

# ---------- Utility functions ----------

def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()

def read_line_from_account_file():
    '''Function to read a line from the accounts file but not the last newline character.
       Note: The account_file must be open to read from for this function to succeed.'''
    global account_file
    return account_file.readline()[0:-1]

def plot_interest_graph():
    '''Function to plot the cumulative interest for the next 12 months here.'''

    # YOUR CODE to generate the x and y lists here which will be plotted
    
    x=[1,2,4,5,6,7,8,9,10,11,12]
    y=[]
    p = float(account.balance)
    print(p)
    rate = float(account.interest_rate)
    for val in x:
        value=(p*1*rate)/100
        y.append(p+value)
        p+=value
    
    # This code to add the plots to the window is a little bit fiddly so you are provided with it.
    # Just make sure you generate a list called 'x' and a list called 'y' and the graph will be plotted correctly.
    figure = Figure(figsize=(5,2), dpi=100)
    figure.suptitle('Cumulative Interest 12 Months')
    a = figure.add_subplot(111)
    a.plot(x, y, marker='o')
    a.grid()
    
    canvas = FigureCanvasTkAgg(figure, master=win)
    canvas.draw()
    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=4, column=0, columnspan=5, sticky='nsew')


# ---------- UI Screen Drawing Functions ----------
def create_login_screen():
    '''Function to create the login screen.'''
         
    global pin_number_var, account_pin_entry, account_number_var, account_number_entry
    
    # ----- Row 0 -----
    # 'FedUni Banking' label here. Font size is 32.
    fedlbl = tk.Label(win,text='FedUni Banking',font=('Arial',32))
    fedlbl.grid(row=0, column=0, columnspan=3)    

    # ----- Row 1 -----
    # Acount Number / Pin label here
    acc_pin_lbl = tk.Label(win, text='Account Number/Pin', font=('Arial',10))
    acc_pin_lbl.grid(row=1, column=0, sticky='nsew')

    # Account number entry here
    account_number_var = tk.StringVar()
    account_number_entry = tk.Entry(win, textvariable=account_number_var,font=('Arial',10))
    account_number_entry.focus_set()
    account_number_entry.grid(row=1, column=1, sticky='nsew')    
    
    # Account pin entry here
    pin_number_var = tk.StringVar()
    account_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var,show='*')
    account_pin_entry.grid(row=1, column=2, sticky='nsew')
    

    # ----- Row 2 -----
    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn1 = tk.Button(win, text='1',font=('Arial',18))
    btn1.bind('<Button-1>', handle_pin_button)
    btn1.grid(row=2, column=0, sticky='nsew')
    
    btn2 = tk.Button(win, text='2',font=('Arial',18))
    btn2.grid(row=2, column=1, sticky='nsew')
    btn2.bind('<Button-1>', handle_pin_button)
    
    btn3 = tk.Button(win, text='3',font=('Arial',18))
    btn3.grid(row=2, column=2, sticky='nsew')
    btn3.bind('<Button-1>', handle_pin_button)

    # ----- Row 3 -----
    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn3 = tk.Button(win, text='4',font=('Arial',18))
    btn3.bind('<Button-1>', handle_pin_button)
    btn3.grid(row=3, column=0, sticky='nsew')
    
    btn4 = tk.Button(win, text='5',font=('Arial',18))
    btn4.grid(row=3, column=1, sticky='nsew')
    btn4.bind('<Button-1>', handle_pin_button)
    
    btn5 = tk.Button(win, text='6',font=('Arial',18))
    btn5.grid(row=3, column=2, sticky='nsew')
    btn5.bind('<Button-1>', handle_pin_button)
    
    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    btn7 = tk.Button(win, text='7',font=('Arial',18))
    btn7.bind('<Button-1>', handle_pin_button)
    btn7.grid(row=4, column=0, sticky='nsew')
    
    btn8 = tk.Button(win, text='8',font=('Arial',18))
    btn8.grid(row=4, column=1, sticky='nsew')
    btn8.bind('<Button-1>', handle_pin_button)
    
    btn9 = tk.Button(win, text='9',font=('Arial',18))
    btn9.grid(row=4, column=2, sticky='nsew')
    btn9.bind('<Button-1>', handle_pin_button)
    
    # ----- Row 5 -----
    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    clrbtn = tk.Button(win,text='Cancel/Clear',bg='red',activebackground='red')
    clrbtn.bind('<Button-1>',clear_pin_entry)
    clrbtn.grid(row=5,column=0,sticky='nsew')
    
    # Button 0 here    
    btn0 = tk.Button(win, text='0',font=('Arial',18))
    btn0.grid(row=5, column=1, sticky='nsew')
    btn0.bind('<Button-1>', handle_pin_button)
                      

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    loginbtn = tk.Button(win,text='logIn',bg='green',activebackground='green',font=('Arial',18))
    loginbtn.grid(row=5,column=2,sticky='nsew')
    loginbtn.bind('<Button-1>',log_in)     

    # ----- Set column & row weights -----
    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)
    win.rowconfigure(5, weight=1)
    
def create_account_screen():
    '''Function to create the account screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var
    global account_number_var,amount_entry_var,transaction_text_widget_var
    
    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
     # ----- Row 0 -----
    # 'FedUni Banking' label here. Font size is 32.
    fedlbl = tk.Label(win,text='FedUni Banking',font=('Arial',24))
    fedlbl.grid(row=0, column=0, columnspan=5,sticky='nsew')    

    # ----- Row 1 -----

    # Account number label here
    acc_num_lbl = tk.Label(win, text='Account Number:'+account.account_number, font=('Arial',10))
    acc_num_lbl.grid(row=1, column=0, sticky='nsew')    

    # Balance label here
    balance_var = tk.StringVar()
    balance_label = tk.Label(win, textvariable=balance_var)    
    #acc_balance = tk.Label(win, text='Balance:'+account.balance, font=('Arial',10))    
    balance_var.set('Balance: $'+account.balance)
    balance_label.grid(row=1, column=1,columnspan=1, sticky='nsew') 

    # Log out button here
    lb = tk.Button(win,command=save_and_log_out, text='logout')
    lb.grid(row=1, column=2,columnspan=2, sticky='nsew')    
    

    # ----- Row 2 -----

    # Amount label here    
    amountlbl = tk.Label(win, text='Amount($)', font=('Arial',10))
    amountlbl.grid(row=2, column=0, sticky='nsew') 

    # Amount entry here
    amount_entry_var = tk.StringVar()
    amount_entry = tk.Entry(win, textvariable=amount_entry_var)
    amount_entry.grid(row=2, column=1, sticky='nsew') 
    

    # Deposit button here
    depositbtn = tk.Button(win, text="Deposit",command=perform_deposit)
    #depositbtn.bind('<Button-1>',save_and_log_out)
    depositbtn.grid(row=2, column=2,columnspan=1, sticky='nsew')
    

    # Withdraw button here
    
    withdrawbtn = tk.Button(win, text="Withdraw",command=perform_withdrawal)
    #withdrawbtn.bind('<Button-1>',account.withdraw_funds)
    withdrawbtn.grid(row=2, column=3,columnspan=1, sticky='nsew')

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.
    
    
    # ----- Row 3 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)
    scrollbar = Scrollbar(win,orient='vertical')
    scrollbar.grid(row=3,column=3,sticky='nse')
    #scrollbar.pack( side = RIGHT, fill = Y )
    
    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    transaction_text_widget_var = tk.StringVar()
    transaction_text_widget = tk.Text(win, state='disabled', height=10, width=48, yscrollcommand = scrollbar.set)
    transaction_text_widget.grid(row=3,column=0,columnspan=4,sticky='w')
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited    transaction_string = account.get_transaction_string()        
    transaction_string = account.get_transaction_string()
    transaction_text_widget.config(state='normal')
    transaction_text_widget.delete(1.0,END)
    transaction_text_widget.insert(INSERT, str(transaction_string))            
    transaction_text_widget.config(state='disabled') 

    # Now add the scrollbar and set it to change with the yview of the text widget
    scrollbar.config( command = transaction_text_widget.yview )


    # ----- Row 4 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_interest_graph()
    

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 5 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    
    win.columnconfigure(0, weight=3)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.columnconfigure(3, weight=3)
    win.columnconfigure(4, weight=3)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)


# ---------- Display Login Screen & Start Main loop ----------

create_login_screen()
#create_account_screen()
win.mainloop()
