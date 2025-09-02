import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from decimal import Decimal
import pytest
import data

@pytest.fixture(autouse=True)
def reset_balance():
    """
    Reset the balance before and after each test to avoid test coupling.
    """
    data.write_balance(Decimal("1000.00"))
    yield
    data.write_balance(Decimal("1000.00"))
