"""
Operations module for the Account Management System.

This module provides the core account operations:
- View the current balance
- Credit the account
- Debit the account
- Execute operations based on user input

It interacts with the `data` module to read and update the balance.
"""

from decimal import Decimal, InvalidOperation
import data


def _parse_amount(prompt: str) -> Decimal | None:
    """
    Ask the user for a monetary amount and validate the input.
    Args:
        prompt (str): The message shown to the user when asking for input.
    Returns:
        Decimal | None: The parsed and rounded amount if valid, 
                        or None if the input is invalid or not positive.
    """
    raw = input(prompt).strip()
    try:
        amt = Decimal(raw)
    except InvalidOperation:
        print("Invalid amount.")
        return None
    if amt <= 0:
        print("Amount must be positive.")
        return None
    return amt.quantize(Decimal("0.01"))


def total() -> None:
    """
    Display the current account balance.
    """
    balance = data.read_balance()
    print(f"Current balance: {balance:.2f}")


def credit() -> None:
    """
    Credit the account with a positive amount entered by the user.
    - Prompts the user for an amount.
    - If valid, adds it to the current balance and updates storage.
    - Prints the new balance.
    """
    amount = _parse_amount("Enter credit amount: ")
    if amount is None:
        return
    balance = data.read_balance()
    new_balance = (balance + amount).quantize(Decimal("0.01"))
    data.write_balance(new_balance)
    print(f"Amount credited. New balance: {new_balance:.2f}")


def debit() -> None:
    """
    Debit the account with a positive amount entered by the user.
    - Prompts the user for an amount.
    - If valid and funds are sufficient, subtracts from the balance and updates storage.
    - Prints the new balance or an error message if funds are insufficient.
    """
    amount = _parse_amount("Enter debit amount: ")
    if amount is None:
        return
    balance = data.read_balance()
    if balance >= amount:
        new_balance = (balance - amount).quantize(Decimal("0.01"))
        data.write_balance(new_balance)
        print(f"Amount debited. New balance: {new_balance:.2f}")
    else:
        print("Insufficient funds for this debit.")


def execute(operation: str) -> None:
    """
    Execute an operation by name.
    Args:
        operation (str): The operation to execute. 
                         Accepted values are "TOTAL", "CREDIT", "DEBIT".
    Behavior:
        - TOTAL → Show current balance
        - CREDIT → Credit the account
        - DEBIT → Debit the account
        - Any other input → Print an error message
    """
    op = operation.strip().upper()
    if op == "TOTAL":
        total()
    elif op == "CREDIT":
        credit()
    elif op == "DEBIT":
        debit()
    else:
        print("Invalid operation.")
