import pymysql
from datetime import datetime

# MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="your_password_here",
    database="Bank_manage_sys")
cursor = db.cursor()

# ---------- USER FUNCTIONS ----------
def register_user():
    while True:
        name = input("Enter Name: ")
        if name.isalpha():   
            break
        else:
            print("Invalid name")

    acc_type = input("Enter Account Type (Savings/Current): ")
    pin = input("Set 4-digit PIN: ")
    balance = float(input("Enter Initial Deposit: "))

    cursor.execute(
        "INSERT INTO users (name, account_type, pin, balance) VALUES (%s, %s, %s, %s)",
        (name, acc_type, pin, balance))
    db.commit()

    acc_no = cursor.lastrowid
    account_number = str(acc_no).zfill(12)
    print("Registration successful!")
    print("Your Account Number is:", account_number)

def user_login():
    acc_no = input("Enter Account Number: ")
    pin = input("Enter PIN: ")
    cursor.execute("SELECT * FROM users WHERE account_no=%s AND pin=%s", (acc_no, pin))
    user = cursor.fetchone()
    if user:
        print(f"Welcome {user[1]}!")
        user_menu(acc_no)
    else:
        print("Invalid Account Number or PIN")


def view_account(acc_no):
    cursor.execute("SELECT * FROM users WHERE account_no=%s", (acc_no,))
    user = cursor.fetchone()
    account_number = str(user[0]).zfill(12)
    print(f"Name: {user[1]}, Account No: {account_number}, Type: {user[2]}, Balance: {user[4]}")


def debit_amount(acc_no):
    amount = float(input("Enter amount to debit: "))
    cursor.execute("SELECT balance FROM users WHERE account_no=%s", (acc_no,))
    bal = float(cursor.fetchone()[0])

    if amount <= bal:
        new_bal = bal - amount
        cursor.execute("UPDATE users SET balance=%s WHERE account_no=%s", (new_bal, acc_no))
        cursor.execute(
            "INSERT INTO transactions (account_no, action, amount, trans_date) VALUES (%s,%s,%s,%s)",
            (acc_no, 'Debit', amount, datetime.now())
        )
        db.commit()
        print("Amount debited successfully!")
    else:
        print("Insufficient balance")

def credit_amount(acc_no):
    amount = float(input("Enter amount to credit: "))
    cursor.execute("SELECT balance FROM users WHERE account_no=%s", (acc_no,))
    bal = float(cursor.fetchone()[0])

    new_bal = bal + amount
    cursor.execute("UPDATE users SET balance=%s WHERE account_no=%s", (new_bal, acc_no))
    cursor.execute(
        "INSERT INTO transactions (account_no, action, amount, trans_date) VALUES (%s,%s,%s,%s)",
        (acc_no, 'Credit', amount, datetime.now())
    )
    db.commit()
    print("Amount credited successfully!")


def change_pin(acc_no):
    old_pin = input("Enter old PIN: ")
    cursor.execute("SELECT pin FROM users WHERE account_no=%s", (acc_no,))
    current_pin = cursor.fetchone()[0]
    if old_pin == current_pin:
        new_pin = input("Enter new PIN: ")
        cursor.execute("UPDATE users SET pin=%s WHERE account_no=%s", (new_pin, acc_no))
        db.commit()
        print("PIN changed successfully!")
    else:
        print("Old PIN incorrect.")


def statement(acc_no):
    cursor.execute("SELECT * FROM transactions WHERE account_no=%s", (acc_no,))
    for row in cursor.fetchall():
        print(row)

def user_menu(acc_no):
    while True:
        print("\n1. View Account\n2. Debit\n3. Credit\n4. Change PIN\n5. Statement\n6. Logout")
        ch = input("Enter choice: ")
        if ch == '1':
            view_account(acc_no)
        elif ch == '2':
            debit_amount(acc_no)
        elif ch == '3':
            credit_amount(acc_no)
        elif ch == '4':
            change_pin(acc_no)
        elif ch == '5':
            statement(acc_no)
        elif ch == '6':
            break
        else:
            print("Invalid choice.")

# ---------- ADMIN FUNCTIONS ----------
def admin_login():
    admin_id = input("Enter Admin ID: ")
    password = input("Enter Password: ")
    cursor.execute("SELECT * FROM admin WHERE admin_id=%s AND password=%s", (admin_id, password))
    if cursor.fetchone():
        print("Admin Login Successful!")
        admin_menu()
    else:
        print("Invalid Admin Login")

def view_all_users():
    cursor.execute("SELECT * FROM users")
    for user in cursor.fetchall():
        acc_no = str(user[0]).zfill(12)
        print(f"Account No: {acc_no}, Name: {user[1]}, Type: {user[2]}, Balance: {user[4]}")

def view_user_details():
    acc_no = input("Enter Account Number: ")
    cursor.execute("SELECT * FROM users WHERE account_no=%s", (acc_no,))
    user = cursor.fetchone()
    if user:
        acc_no = str(user[0]).zfill(12)
        print(f"Account No: {acc_no}, Name: {user[1]}, Type: {user[2]}, Balance: {user[4]}")

def view_user_transactions():
    acc_no = input("Enter Account Number: ")
    cursor.execute("SELECT * FROM transactions WHERE account_no=%s", (acc_no,))
    for row in cursor.fetchall():
        print(row)

def view_day_transactions():
    date = input("Enter Date (YYYY-MM-DD): ")
    cursor.execute("SELECT * FROM transactions WHERE DATE(trans_date)=%s", (date,))
    for row in cursor.fetchall():
        print(row)

def admin_menu():
    while True:
        print("\n1. View All Users\n2. View User Details\n3. View User Transactions\n4.View Day Transactions\n5. Logout")
        ch = input("Enter choice: ")
        if ch == '1':
            view_all_users()
        elif ch == '2':
            view_user_details()
        elif ch == '3':
            view_user_transactions()
        elif ch == '4':
            view_day_transactions()
        elif ch == '5':
            break
        else:
            print("Invalid choice.")

# ---------- MAIN ----------
while True:
    print("\n--- Bank Management System ---")
    print("1. Register User\n2. User Login\n3. Admin Login\n4. Exit")
    choice = input("Enter choice: ")
    if choice == '1':
        register_user()
    elif choice == '2':
        user_login()
    elif choice == '3':
        admin_login()
    elif choice == '4':
        break
    else:
        print("Invalid choice.")
