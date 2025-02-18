# An application to do bank operations like :

    # 1. Create a new account
    # 2. Check balance of current savings account
    # 3. Withdraw money from account
    # 4. Delete your savings account
    # 5. Transfer cash to another account in the same bank
    # 6. Check for loan eligibility
    # 7. Change passsword for withdrawal of money
    # 8. Show full account details by login to your profile
    # 9. To repay the Loan Amount
    # 9. Exit

import random
import os
import json
from datetime import datetime, timedelta

class ABC_BANK:

    def __init__(self):

        self.bank_data_file="bank_data.json"
        self.bank_accounts=self.load_data()

    def load_data(self):

        if os.path.exists(self.bank_data_file):
            with open(self.bank_data_file,"r") as file:
                try:
                    data=json.load(file)
                    return{str(k):v for k,v in data.items()}
                except json.JSONDecodeError:
                    print("Error Loading JSON file. Resetting data")
                    return{}
        else:
            print("\n New file was created")
            return{}

    def save_data(self):

        with open(self.bank_data_file,"w") as file:
            json.dump(self.bank_accounts,file,indent=4)

        self.bank_accounts=self.load_data()

    def calculate_interest(self,acc):

        acc=str(acc)

        if acc not in self.bank_accounts:
            return

        account = self.bank_accounts[acc]
        last_interest_date = datetime.strptime(account["last_interest_date"], "%Y-%m-%d")
        current_date = datetime.today()
        days_passed = (current_date - last_interest_date).days

        if days_passed > 0:

            interest_rate_savings = 0.04  
            daily_interest_savings = (account["balance"] * interest_rate_savings) / 365
            account["balance"] += round(daily_interest_savings * days_passed, 2)  

            interest_rate_loan=0.08
            if account['loan']>0:

                daily_interest_loan=(account['loan']*interest_rate_loan)/365
                account['loan']+=round(daily_interest_loan*days_passed,2)

            account["last_interest_date"] = current_date.strftime("%Y-%m-%d")
            self.save_data()

    def new_account(self):

        name=input("\nEnter your name : ")

        while True:
            try:
                ph_no=int(input("\nEnter your phone number :"))

                if len(str(ph_no))==10:

                    print("\n   Phone number added sucessfully ")
                    break

                else:
                    print("\n   invalid phone number , try again")

            except ValueError:
                print("\n Invalid input , please enter a 10 digit number")

        while True:

            try:

                password=int(input("\nEnter a 4 digit pin for your Transactions : "))

                if len(str(password))==4:

                    print("\nPassword created successfully")
                    break

                else:
                    print("\n Enter a valid Pin number")

            except ValueError:

                print("\n Invalid input , please enter a 4 digit number ")

        while True:

            account_no=random.randint(100000, 999999)

            if account_no not in self.bank_accounts:

                break

        while True:

            try:
                balance=int(input("\nEnter the amount you want to deposit to your accound : "))

                if balance>0:

                    break

                else:

                    print("\nDeposit amount must be greater than zero")

            except ValueError:

                print("\n Invalid input , please try again")

        self.bank_accounts[account_no]={"name":name,
                                        "phone_number":ph_no,
                                        "password":password,
                                        "balance":balance,
                                        "loan":0,
                                        "last_interest_date":datetime.today().strftime("%Y-%m-%d")}
        
        self.save_data()
        print(f"\n  Account created sucessfully , your account number is {account_no} and name is {name} \n     == Please note account number for further Bank Services ==")


    def balance(self):
        
        if not self.bank_accounts:

            print("No account Found")
            return

        try: 

            acc=int(input("\n   Enter your account number : "))
            peru=input("\n   Enter your name : ") 

            for i,j in self.bank_accounts.items():
                self.save_data()
                if i==str(acc) and j['name'].lower()==peru.lower():
                    try:
                        pin=int(input("\nEnter your 4 digit pin : "))
                        if pin==j['password']:
                            self.calculate_interest(i)

                            print(f"\n Your available balance is {j['balance']}")
                            return
                        else:
                            print("\nInvalid PIN")
                            return
                    except ValueError:
                        print("\nInvalid Input. PIN must be 4 digit numeric value.")
                        return

            print("\nAccount number or name doesnot match")

        except ValueError:

            print("\nInvalid account number , please enter a numeric value")


    def withdraw(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            acc=int(input("\n   Enter your account number : "))
            peru=input("\n  Enter your name : ")

            for i,j in self.bank_accounts.items():

                if i==str(acc) and j['name'].lower()==peru.lower():

                    self.calculate_interest(i)

                    try:

                        amount=int(input("\nHow much money do you want to withdraw :"))
                        pin=int(input("\nEnter your 4 digit pin : "))

                        if pin!=j['password']:

                            return print("\nInvalid pin, please try again")
                            

                        if amount<=0:

                            return print("\nWithdrawal amount must be greater than zero")
                            

                        if j['balance']-100>=amount:

                            j['balance']-=amount
                            self.save_data()

                            print(f"\nWithdrawal successful! Your new balance is {j['balance']}")
                            return

                        else:
                            print("\nInsufficient Fund, please try again with a less amount")
                            return

                    except ValueError:

                        print("\nInvalid amount, please eneter a numeric value")

            else:
                print("\nAccount number not found")

        except ValueError:

            print("\ninvalid account number, please enter a numeric value")

    
    def deposit(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():
                self.calculate_interest(i)

                if i==str(acc):

                    try:

                        money=int(input("\nHow much money you want to deposit : "))

                        if money>0:

                            pas=int(input("\nEnter your 4 digit pin : "))

                            if pas==j['password']:

                                j['balance']+=money
                                self.save_data()

                                print(f"\nDeposit complete , new balance is {j['balance']}")
                                return
                            
                            else:

                                print("\nEnter pin is incorrect, try again")
                                return

                        else:

                            print("Entered amount should be greater than zero, try again")
                            return
                        
                    except ValueError:

                        print("\nInvalid input , please enter numeric value as deposit amount")
            else:

                print("\nAccount number mismatch")
                return
        
        except ValueError:

            print("\n Invalid account number")


    def delete(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            name=input("\n  Enter your name : ")
            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():

                if i==str(acc) and j['name'].lower()==name.lower():
                    self.calculate_interest(i)

                    yes=input("\nEnter 'yes' to withdraw the cash and delete the account : ")
                    
                    if yes.lower() == "yes":
                        try:

                            pin=int(input("\nEnter your 4 digit pin : "))

                            if pin==j['password']:

                                print(f"\nWithdrawing available balance {j['balance']}")
                                j['balance']=0

                                print("\nAmount Withdrawn Sucessfully , Proceding to delete account")

                                del self.bank_accounts[i]
                                self.save_data()

                                print(f"Your account {i} has been deleted")
                                return

                            else:
                                print("\nInvalid input! PIN must be a 4-digit numeric value.")
                                return
                            
                        except ValueError:
                            print("\n Invalid input . Enter 4 digit numeric PIN.")
                            return

                    else:
                        print("\nInvalid Operation, account not deleted")

            else:
                print("\nAccount Not Found,please check details and try again")
                return

        except ValueError:

            print("\nInvalid input for account number, please enter numeric value")

    
    def change_password(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():

                if str(acc)==i:

                    old_pass=input("\nEnter your old password : ")

                    if old_pass.isdigit():
                        old_pass=int(old_pass)
                    else:
                
                        print("\nInvalid old password, please enter numeric value")
                        return

                    if old_pass==j['password']:

                        new_pass=input("\nEnter your 4 digit new password : ")

                        if new_pass.isdigit() and len(new_pass) == 4:

                            j['password']=int(new_pass)
                            self.save_data()
                            print("\nPassword changed sucessfully")
                            return                                              

                        else:
                            print("\nEntered new password should only contain 4 numeric digit")
                            return

                    else:
                        print("\nInvalid old Password")
                        return

            else:
                print("\nAccount number not found")

        except ValueError:
            print("\nInvalid account number, please enter numeric values")


    def transfer(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():

                if i==str(acc):
                    self.calculate_interest(i)

                    pin=int(input("\nEnter your 4 digit PIN : "))

                    if pin!=j['password']:
                        print("\nInvalid PIN, please try again")
                        return

                    transfer_account=int(input("\nEnter the account number to which you have to send the money : "))

                    if str(transfer_account)==i:
                        print("\nYou Cannot transfer money to the same account")
                        return
                    
                    transfer_name=input("\nEnter the name of the account holder : ")

                    for k,l in self.bank_accounts.items():

                        if k==str(transfer_account) and l['name'].lower()==transfer_name.lower():
                            try:

                                transfer_amount=float(input("\nEnter the amount you want to send : "))
                                if transfer_amount<=0:
                                    print("\nTransfer amount must be greater than zero.")
                                    return

                                if j['balance']-transfer_amount>=100:

                                    l['balance']+=transfer_amount
                                    j['balance']-=transfer_amount
                                    self.save_data()

                                    print(f"\nAmount transferred sucessfully , your available balance is {j['balance']}")
                                    return

                                else:
                                    print("\nInsufficient balance & Minimum ₹100 must be maintained in the account.")
                                    return
                            
                            except ValueError:
                                print("\nInvalid amount. Please enter a numeric value")
                                return
                    else:

                        print("\n The recepient details not found in data base, please check again. Thank You")
                        return

            else:

                print("\nAccount Number doesn't exists, please check again")
                return

        except ValueError:

            print("\n Invalid account number, please enter numeric digits")


    def account_details(self):

        if not self.bank_accounts:

            print("No account Found")
            return
        
        try:

            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():

                if i==str(acc):

                    try:
                        pin=int(input("\n Enter your PIN : "))
                        if pin==j['password']:
                            self.calculate_interest(i)

                            print("\n  ===  Your Account Details  ===  \n")
                            print(f" Name              : {j['name']}")
                            print(f" Account Number    : {i} ")
                            print(f" Phone number      : {j['phone_number']}")
                            print(f" Available Balance : {j['balance']}")

                            if j['loan']>0:

                                print(f" Loan Taken        : {j['loan']}")

                            else:

                                print(f" No Loan Taken")

                            print(self.bank_accounts)

                            return

                        else:
                            print("\nInvalid PIN, please try again")
                            return
                        
                    except ValueError:
                        print("\nInvalid input! PIN must be a 4-digit numeric value.")
                        return

            print("\n Account Number Not Found")
            return

        except ValueError:
            print("\nInvalid Input. Please enter a numeric account number.")

    
    def loan_eligibility(self):

        if not self.bank_accounts:

            print("No account Found")
            return

        try:

            acc=int(input("\n   Enter your account number : "))

            for i,j in self.bank_accounts.items():
                self.calculate_interest(i)

                if i==str(acc):

                    loan_options={
                        (20000,40000):100000,
                        (40000, 60000): 200000,
                        (60000, 100000): 300000,
                        (100000, float('inf')): 400000}
                    
                    for(min_balance,max_balance),loan_amount in loan_options.items():

                        if min_balance<=j['balance']<max_balance:

                            print(f"\n You are eligible for a loan of ₹{loan_amount}")
                            answer=input("\n Do You want to take the loan (yes/no) ?").strip().lower()

                            if answer == "yes":
                                try:
                                    pin=int(input("\n Enter your PIN for conformation: "))
                                    if pin==j['password']:

                                        j['loan']+=loan_amount
                                        self.save_data()
                                        print(f"\nLoan Amount successfully added to your bank account. New loan amount is ₹{j['loan']}.")

                                    else:
                                        print("\nInvalid Password, Please try again.")
                                        return
                                except ValueError:
                                    print("\nInvalid input! PIN must be a 4-digit numeric value.")
                                    return

                            else:
                                print("\nLoan Declined")

                            return
                        
                    print("\nYou are not eligible for Loan")
                    return
                
            else:
                print("\n Account number not found")
                return

        except ValueError:

            print("\n Invalid account number, please enter numeric digits")
            return


    def repay_loan(self):
    
        if not self.bank_accounts:
            print("No accounts found.")
            return

        try:
            acc = int(input("\nEnter your account number: "))

            for i, j in self.bank_accounts.items():

                if i == str(acc):

                    self.calculate_interest(i) 

                    if j["loan"] == 0:
                        print("\nYou do not have any active loans to repay.")
                        return

                    print(f"\nYour current loan balance is ₹{j['loan']}.")

                    try:
                        repay_amount = float(input("Enter the amount you want to repay: "))

                        if repay_amount <= 0:
                            print("\nRepayment amount must be greater than zero.")
                            return

                        if repay_amount > j["balance"]:
                            print("\nInsufficient balance to repay this amount.")
                            return

                        if repay_amount > j["loan"]:
                            print("\nRepayment amount exceeds loan balance.")
                            return

                        try:
                            pin = int(input("\nEnter your 4-digit PIN: "))

                            if pin != j["password"]:
                                print("\nIncorrect PIN! Loan repayment denied.")
                                return

                        except ValueError:
                            print("\nInvalid PIN format! Please enter a 4-digit numeric PIN.")
                            return
                        
                        j["balance"] -= repay_amount
                        j["loan"] -= repay_amount
                        self.save_data()

                        print(f"\nSuccessfully repaid ₹{repay_amount}. Remaining loan balance: ₹{j['loan']}")

                        if j["loan"] == 0:
                            print("\nCongratulations! You have fully repaid your loan.")

                        return

                    except ValueError:
                        print("\nInvalid input! Please enter a valid numeric repayment amount.")
                        return

            print("\nAccount number not found.")

        except ValueError:
            print("\nInvalid input! Please enter a numeric account number.")


obj1=ABC_BANK()

while True:

    print("\n\n---    Welcome to ABC Bank intercative application, i am here to help you  ---\n")
    new=input("         Are you a current customer or not  (yes / no ) : ").strip().lower()

    if new=="yes":

        print("\n1. Check balance of current savings account")
        print("2. Withdraw money from account")
        print("3. Delete your savings account")
        print("4. Transfer cash to another account in the same bank")
        print("5. Check for loan eligibility")
        print("6. Change password for withdrawal of money")
        print("7. Show Account details by Login to your profile")
        print("8. Deposit Money")
        print("9. Repay Loan")
        print("10. Exit\n")

        try:
            choice=int(input("Enter the operation you want to do : "))

        except ValueError:
            print("\nInvalid input ! Please enter a numeric option.")
            continue

        if choice==1:
            
            obj1.balance()

        elif choice==2:

            obj1.withdraw()

        elif choice==3:

            obj1.delete()

        elif choice==4:

            obj1.transfer()

        elif choice==5:

            obj1.loan_eligibility()

        elif choice==6:

            obj1.change_password()

        elif choice==7:

            obj1.account_details()

        elif choice==8:

            obj1.deposit()

        elif choice==9:

            obj1.repay_loan()

        elif choice==10:

            print("\n~~~   Thank You for using ABC Bank. Goodbye!  ~~~\n\n")
            break

        else:
            print("\nInvalid choice! Please select a valid option.")

    elif new=="no":

        print("\n1. Create a new account")
        print("2. Exit")

        try:
            choice2=int(input("\nEnter the operation you want to do : "))

        except ValueError:
            print("\nInvalid input! Please enter a numeric option.")
            continue
    
        if choice2==1:

            obj1.new_account()

        elif choice2==2:

            print("\n~~~   Thank You for visiting ABC Bank. Goodbye!  ~~~\n")
            break

        else:

            print("\nInvalid choice! Please select a valid option")

    else:
        print("\nInvalid operation , Please enter 'yes' or 'no' .\n")
        a=input("Do you want to exit (yes / no) : ").strip().lower()

        if a=="no":

            continue

        else:

            break
