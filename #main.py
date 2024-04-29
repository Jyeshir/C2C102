#main
import mysql.connector

class OnlineBankingSystem:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root',
            database='c2c_project',
            password='2gd4Fart$'
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        return user

    def check_account_balance(self, user_id):
        query = "SELECT balance FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def deposit_funds(self, user_id, amount):
        update_query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
        self.cursor.execute(update_query, (amount, user_id))
        self.connection.commit()
        insert_query = "INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'deposit', %s)"
        self.cursor.execute(insert_query, (user_id, amount))
        self.connection.commit()

    def withdraw_funds(self, user_id, amount):
        select_query = "SELECT balance FROM users WHERE user_id = %s"
        self.cursor.execute(select_query, (user_id,))
        result = self.cursor.fetchone()
        if result:
            balance = result[0]
            if balance >= amount:
                update_query = "UPDATE users SET balance = balance - %s WHERE user_id = %s"
                self.cursor.execute(update_query, (amount, user_id))
                self.connection.commit()
                insert_query = "INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'withdrawal', %s)"
                self.cursor.execute(insert_query, (user_id, amount))
                self.connection.commit()
                return True
            else:
                return False
        else:
            return False

    def create_new_account(self, username, password, email, full_name):
        insert_query = "INSERT INTO users (username, password, email, full_name) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(insert_query, (username, password, email, full_name))
        self.connection.commit()

    def delete_account(self, user_id):
        delete_transactions_query = "DELETE FROM transactions WHERE user_id = %s"
        self.cursor.execute(delete_transactions_query, (user_id,))
        self.connection.commit()
        delete_user_query = "DELETE FROM users WHERE user_id = %s"
        self.cursor.execute(delete_user_query, (user_id,))
        self.connection.commit()

    def modify_account_details(self, user_id, new_email, new_password, new_full_name):
        update_query = "UPDATE users SET email = %s, password = %s, full_name = %s WHERE user_id = %s"
        self.cursor.execute(update_query, (new_email, new_password, new_full_name, user_id))
        self.connection.commit()

    def get_user_transactions(self, user_id):
        query = "SELECT * FROM transactions WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        transactions = self.cursor.fetchall()
        return transactions

    def main_menu(self):
        print("Welcome to the Online Banking System")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Create New Account")
        print("5. Close Account")
        print("6. Modify Account")
        print("0. Exit")

    def run(self):
        while True:
            self.main_menu()
            choice = input("Please enter your choice: ")

            if choice == "1":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.authenticate_user(username, password)
                if user:
                    balance = self.check_account_balance(user[0])
                    if balance is not None:
                        print(f"Your current balance is: ${balance:.2f}")
                    else:
                        print("Error: Unable to retrieve balance.")
                else:
                    print("Invalid username or password.")
                    
            elif choice == "2":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.authenticate_user(username, password)
                if user:
                    amount = float(input("Enter the amount you want to deposit: $"))
                    self.deposit_funds(user[0], amount)
                    print(f"${amount:.2f} deposited successfully.")
                else:
                    print("Invalid username or password.")
                    
            elif choice == "3":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.authenticate_user(username, password)
                if user:
                    amount = float(input("Enter the amount you want to withdraw: $"))
                    if self.withdraw_funds(user[0], amount):
                        print(f"${amount:.2f} withdrawn successfully.")
                    else:
                        print("Insufficient balance.")
                else:
                    print("Invalid username or password.")
                    
            elif choice == "4":
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                email = input("Enter an email: ")
                full_name = input("Enter your full name: ")
                self.create_new_account(username, password, email, full_name)
                print("Account created successfully.")
                
            elif choice == "5":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.authenticate_user(username, password)
                if user:
                    self.delete_account(user[0])
                    print("Account closed successfully.")
                else:
                    print("Invalid username or password.")
                    
            elif choice == "6":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                user = self.authenticate_user(username, password)
                if user:
                    new_email = input("Enter your new email: ")
                    new_password = input("Enter your new password: ")
                    new_full_name = input("Enter your new full name: ")
                    self.modify_account_details(user[0], new_email, new_password, new_full_name)
                    print("Account details modified successfully.")
                else:
                    print("Invalid username or password.")
                    
            elif choice == "0":
                print("Thank you for using the Online Banking System. Have a great day!")
                break
                
            else:
                print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    banking_system = OnlineBankingSystem()
    banking_system.run()
