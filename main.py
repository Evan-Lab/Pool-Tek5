"""
Main entry point for the Account Management System.

This script runs the interactive menu that allows the user to:
- View the current balance
- Credit the account
- Debit the account
- Exit the program

It delegates the actual operations to the `operations` module.
"""

import operations


def main() -> None:
    """
    Run the Account Management System.
    This function provides a simple text-based menu that allows the user to:
    1. View the current account balance
    2. Credit the account
    3. Debit the account
    4. Exit the program
    The menu loops until the user selects option 4 (Exit).
    """
    continue_flag = "YES"
    while continue_flag == "YES":
        print("--------------------------------")
        print("Account Management System")
        print("1. View Balance")
        print("2. Credit Account")
        print("3. Debit Account")
        print("4. Exit")
        print("--------------------------------")
        user_choice = input("Enter your choice (1-4): ").strip()

        if user_choice == "1":
            operations.execute("TOTAL")
        elif user_choice == "2":
            operations.execute("CREDIT")
        elif user_choice == "3":
            operations.execute("DEBIT")
        elif user_choice == "4":
            continue_flag = "NO"
        else:
            print("Invalid choice, please select 1-4.")
    print("Exiting the program. Goodbye!")


if __name__ == "__main__":
    main()
