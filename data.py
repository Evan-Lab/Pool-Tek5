"""
Data module for the Account Management System.

This module provides in-memory storage for the account balance
and functions to read and update it.
"""

from decimal import Decimal
"""
Ixn-memory storage for the account balance.
"""
_STORAGE_BALANCE: Decimal = Decimal("1000.00")


def read_balance() -> Decimal:
    """
    Return the current account balance.
    Returns:
        Decimal: The current balance stored in memory.
    """
    return _STORAGE_BALANCE


def write_balance(balance: Decimal) -> None:
    """
    Update the account balance.
    Args:
        balance (Decimal): The new balance to store.
                           The value is rounded to 2 decimal places.
    """
    global _STORAGE_BALANCE
    _STORAGE_BALANCE = balance.quantize(Decimal("0.01"))
