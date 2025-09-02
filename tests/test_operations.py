from decimal import Decimal
import builtins

import pytest
import data
import operations 

def _set_input(monkeypatch, values):
    """
    Helper to mock input() with predefined values.
    """
    it = iter(values)
    monkeypatch.setattr(builtins, "input", lambda _: next(it))

def test_view_current_balance(capsys):
    """
    TC-1.1: Verify that the current balance is displayed correctly.
    """
    data.write_balance(Decimal("1234.56"))
    operations.total()
    out = capsys.readouterr().out
    assert "Current balance: 1234.56" in out

def test_credit_valid_amount(monkeypatch, capsys):
    """
    TC-2.1: Verify that the account is credited with a valid amount.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["50.00"])
    operations.credit()
    out = capsys.readouterr().out
    assert "Amount credited. New balance: 150.00" in out
    assert data.read_balance() == Decimal("150.00")

def test_credit_zero_amount(monkeypatch, capsys):
    """
    TC-2.2: Verify that the balance remains unchanged when crediting zero.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["0.00"])
    operations.credit()
    out = capsys.readouterr().out
    assert "Amount must be positive." in out
    assert data.read_balance() == Decimal("100.00")

def test_debit_valid_amount(monkeypatch, capsys):
    """
    TC-3.1: Verify that the account is debited with a valid amount.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["50.00"])
    operations.debit()
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 50.00" in out
    assert data.read_balance() == Decimal("50.00")

def test_debit_amount_greater_than_balance(monkeypatch, capsys):
    """
    TC-3.2: Verify that debit greater than balance is rejected.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["2000.00"])
    operations.debit()
    out = capsys.readouterr().out
    assert "Insufficient funds for this debit." in out
    assert data.read_balance() == Decimal("100.00")

def test_debit_zero_amount(monkeypatch, capsys):
    """
    TC-3.3: Verify that the balance remains unchanged when debiting zero.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["0.00"])
    operations.debit()
    out = capsys.readouterr().out
    assert "Amount must be positive." in out
    assert data.read_balance() == Decimal("100.00")


@pytest.mark.parametrize("preset", [Decimal("0.00"), Decimal("12.34"), Decimal("999.99"), Decimal("1000.00")])
def test_TC_1_2_view_balance_various_values(capsys, preset):
    """
    TC-1.2: Verify that different preset balances are displayed correctly.
    """
    data.write_balance(preset)
    operations.total()
    out = capsys.readouterr().out
    assert f"Current balance: {preset:.2f}" in out


@pytest.mark.parametrize(
    "start,amount,new",
    [
        (Decimal("100.00"), "0.01", Decimal("100.01")),
        (Decimal("50.00"), "50.00", Decimal("100.00")),
        (Decimal("10.00"), "90.00", Decimal("100.00")),
        (Decimal("123.45"), "76.55", Decimal("200.00")),
        (Decimal("1.23"), "3.21", Decimal("4.44")),
    ],
)
def test_TC_2_3_credit_multiple_valid(monkeypatch, capsys, start, amount, new):
    """
    TC-2.3: Verify multiple valid credit amounts update balance correctly.
    """
    data.write_balance(start)
    _set_input(monkeypatch, [amount])
    operations.credit()
    out = capsys.readouterr().out
    assert f"Amount credited. New balance: {new:.2f}" in out
    assert data.read_balance() == new


@pytest.mark.parametrize("raw", ["", "abc", "   "])
def test_TC_2_4_credit_invalid_non_numeric(monkeypatch, capsys, raw):
    """
    TC-2.4: Verify that invalid non-numeric credit inputs are rejected.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, [raw])
    operations.credit()
    out = capsys.readouterr().out
    assert "Invalid amount." in out
    assert data.read_balance() == Decimal("100.00")


@pytest.mark.parametrize("raw", ["-1", "-0.01"])
def test_TC_2_5_credit_negative_amount(monkeypatch, capsys, raw):
    """
    TC-2.5: Verify that negative credit amounts are rejected.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, [raw])
    operations.credit()
    out = capsys.readouterr().out
    assert "Amount must be positive." in out
    assert data.read_balance() == Decimal("100.00")


@pytest.mark.parametrize(
    "start,amount,new",
    [
        (Decimal("100.00"), "0.01", Decimal("99.99")),
        (Decimal("100.00"), "10.00", Decimal("90.00")),
        (Decimal("5.00"), "5.00", Decimal("0.00")),
        (Decimal("10.00"), "9.99", Decimal("0.01")),
    ],
)
def test_TC_3_4_debit_multiple_valid(monkeypatch, capsys, start, amount, new):
    """
    TC-3.4: Verify multiple valid debit amounts update balance correctly.
    """
    data.write_balance(start)
    _set_input(monkeypatch, [amount])
    operations.debit()
    out = capsys.readouterr().out
    assert f"Amount debited. New balance: {new:.2f}" in out
    assert data.read_balance() == new


@pytest.mark.parametrize("amount", ["2000.00", "9999", "100.01"])
def test_TC_3_5_debit_insufficient_funds(monkeypatch, capsys, amount):
    """
    TC-3.5: Verify that debit larger than balance shows insufficient funds.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, [amount])
    operations.debit()
    out = capsys.readouterr().out
    assert "Insufficient funds" in out
    assert data.read_balance() == Decimal("100.00")


@pytest.mark.parametrize("amount", ["-1", "-0.01"])
def test_TC_3_6_debit_negative_amount(monkeypatch, capsys, amount):
    """
    TC-3.6: Verify that negative debit amounts are rejected.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, [amount])
    operations.debit()
    out = capsys.readouterr().out
    assert "Amount must be positive." in out
    assert data.read_balance() == Decimal("100.00")


@pytest.mark.parametrize(
    "start,amount",
    [
        (Decimal("100.00"), "100.00"),
        (Decimal("0.01"), "0.01"),
    ],
)
def test_TC_3_7_debit_equal_to_balance(monkeypatch, capsys, start, amount):
    """
    TC-3.7: Verify that debit equal to balance sets balance to zero.
    """
    data.write_balance(start)
    _set_input(monkeypatch, [amount])
    operations.debit()
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 0.00" in out
    assert data.read_balance() == Decimal("0.00")


@pytest.mark.parametrize(
    "op,expected",
    [
        ("TOTAL", "SHOW_TOTAL"),
        ("credit", "DO_CREDIT"),
        ("  DeBiT  ", "DO_DEBIT"),
    ],
)
def test_TC_4_2_execute_dispatch(monkeypatch, capsys, op, expected):
    """
    TC-4.2: Verify that execute() dispatches operations correctly (case-insensitive).
    """
    monkeypatch.setattr(operations, "total", lambda: print("SHOW_TOTAL"))
    monkeypatch.setattr(operations, "credit", lambda: print("DO_CREDIT"))
    monkeypatch.setattr(operations, "debit", lambda: print("DO_DEBIT"))

    operations.execute(op)
    out = capsys.readouterr().out
    assert expected in out


@pytest.mark.parametrize("op", ["", "UNKNOWN", "BALANCEZZ"])
def test_TC_4_3_execute_invalid(capsys, op):
    """
    TC-4.3: Verify that invalid operation names print an error.
    """
    operations.execute(op)
    out = capsys.readouterr().out
    assert "Invalid operation." in out


def test_TC_5_1_sequence_credit_then_debit(monkeypatch):
    """
    TC-5.1: Verify sequence of credit then debit updates balance correctly.
    Start = 100.00 → Credit 25.00 → Debit 10.00 → Final = 115.00
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["25.00"])
    operations.credit()
    _set_input(monkeypatch, ["10.00"])
    operations.debit()
    assert data.read_balance() == Decimal("115.00")


def test_TC_5_2_multiple_credits(monkeypatch):
    """
    TC-5.2: Verify multiple consecutive credits accumulate correctly.
    Start = 0.00 → +10.00 → +20.00 → +30.00 → Final = 60.00
    """
    data.write_balance(Decimal("0.00"))
    _set_input(monkeypatch, ["10.00"])
    operations.credit()
    _set_input(monkeypatch, ["20.00"])
    operations.credit()
    _set_input(monkeypatch, ["30.00"])
    operations.credit()
    assert data.read_balance() == Decimal("60.00")


def test_TC_5_3_multiple_debits(monkeypatch):
    """
    TC-5.3: Verify multiple consecutive debits subtract correctly.
    Start = 200.00 → -50.00 → -50.00 → Final = 100.00
    """
    data.write_balance(Decimal("200.00"))
    _set_input(monkeypatch, ["50.00"])
    operations.debit()
    _set_input(monkeypatch, ["50.00"])
    operations.debit()
    assert data.read_balance() == Decimal("100.00")


def test_TC_6_1_credit_then_insufficient_debit(monkeypatch):
    """
    TC-6.1: Verify that after a credit, an excessive debit is still rejected.
    Start = 50.00 → +25.00 = 75.00 → Try -100.00 → Balance unchanged
    """
    data.write_balance(Decimal("50.00"))
    _set_input(monkeypatch, ["25.00"])
    operations.credit()
    _set_input(monkeypatch, ["100.00"])
    operations.debit()
    assert data.read_balance() == Decimal("75.00")


def test_TC_6_2_debit_to_zero_balance(monkeypatch):
    """
    TC-6.2: Verify debiting the entire balance reduces it to zero.
    Start = 75.00 → -75.00 → Final = 0.00
    """
    data.write_balance(Decimal("75.00"))
    _set_input(monkeypatch, ["75.00"])
    operations.debit()
    assert data.read_balance() == Decimal("0.00")


def test_TC_7_1_execute_mixed_operations(monkeypatch):
    """
    TC-7.1: Verify execute() correctly calls TOTAL, CREDIT, and DEBIT.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["50.00"])
    operations.execute("CREDIT")
    _set_input(monkeypatch, ["25.00"])
    operations.execute("DEBIT")
    operations.execute("TOTAL")
    assert data.read_balance() == Decimal("125.00")


def test_TC_7_2_execute_invalid_trimmed(capsys):
    """
    TC-7.2: Verify execute() rejects invalid operation with spaces.
    """
    operations.execute("   UNKNOWN   ")
    out = capsys.readouterr().out
    assert "Invalid operation." in out


def test_TC_8_1_large_credit(monkeypatch):
    """
    TC-8.1: Verify system handles very large credit values.
    """
    data.write_balance(Decimal("0.00"))
    _set_input(monkeypatch, ["1000000000.00"])
    operations.credit()
    assert data.read_balance() == Decimal("1000000000.00")


def test_TC_8_2_large_debit(monkeypatch):
    """
    TC-8.2: Verify system handles very large debit values when funds are available.
    """
    data.write_balance(Decimal("2000000000.00"))
    _set_input(monkeypatch, ["1999999999.99"])
    operations.debit()
    assert data.read_balance() == Decimal("0.01")

def test_TC_9_1_credit_with_whitespace(monkeypatch, capsys):
    """
    TC-9.1: Credit accepts values with surrounding whitespace.
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["   25.00   "])
    operations.credit()
    out = capsys.readouterr().out
    assert "Amount credited. New balance: 125.00" in out
    assert data.read_balance() == Decimal("125.00")


def test_TC_9_2_debit_with_whitespace(monkeypatch, capsys):
    """
    TC-9.2: Debit accepts values with surrounding whitespace.
    """
    data.write_balance(Decimal("200.00"))
    _set_input(monkeypatch, ["   25.00   "])
    operations.debit()
    out = capsys.readouterr().out
    assert "Amount debited. New balance: 175.00" in out
    assert data.read_balance() == Decimal("175.00")


def test_TC_9_3_credit_invalid_then_valid(monkeypatch):
    """
    TC-9.3: Invalid credit input followed by a valid credit keeps state consistent.
    """
    data.write_balance(Decimal("50.00"))
    _set_input(monkeypatch, ["abc"])
    operations.credit()
    assert data.read_balance() == Decimal("50.00")
    _set_input(monkeypatch, ["25.00"])
    operations.credit()
    assert data.read_balance() == Decimal("75.00")


def test_TC_9_4_debit_negative_then_valid(monkeypatch):
    """
    TC-9.4: Negative debit rejected, then valid debit succeeds.
    """
    data.write_balance(Decimal("80.00"))
    _set_input(monkeypatch, ["-10.00"])
    operations.debit()
    assert data.read_balance() == Decimal("80.00")
    _set_input(monkeypatch, ["30.00"])
    operations.debit()
    assert data.read_balance() == Decimal("50.00")


def test_TC_9_5_execute_total_with_spaces(capsys):
    """
    TC-9.5: execute('   total   ') should call TOTAL after trimming and case-normalization.
    """
    data.write_balance(Decimal("321.00"))
    operations.execute("   total   ")
    out = capsys.readouterr().out
    assert "Current balance: 321.00" in out


def test_TC_9_6_write_balance_quantizes():
    """
    TC-9.6: write_balance quantizes to 2 decimals.
    """
    data.write_balance(Decimal("1.999"))
    assert data.read_balance() == Decimal("2.00")


def test_TC_9_7_credit_then_debit_penny(monkeypatch):
    """
    TC-9.7: Credit 0.01 then debit 0.01 results in 0.00.
    """
    data.write_balance(Decimal("0.00"))
    _set_input(monkeypatch, ["0.01"])
    operations.credit()
    _set_input(monkeypatch, ["0.01"])
    operations.debit()
    assert data.read_balance() == Decimal("0.00")


def test_TC_9_8_alternating_operations(monkeypatch):
    """
    TC-9.8: Alternate credit/debit steps end at expected balance.
    Start 100.00 -> +10.00 -> -5.00 -> +0.50 -> -0.49 -> +4.99 -> -10.00 => 100.00
    """
    data.write_balance(Decimal("100.00"))
    _set_input(monkeypatch, ["10.00"])
    operations.credit()
    _set_input(monkeypatch, ["5.00"])
    operations.debit()
    _set_input(monkeypatch, ["0.50"])
    operations.credit()
    _set_input(monkeypatch, ["0.49"])
    operations.debit()
    _set_input(monkeypatch, ["4.99"])
    operations.credit()
    _set_input(monkeypatch, ["10.00"])
    operations.debit()
    assert data.read_balance() == Decimal("100.00")


def test_TC_9_9_insufficient_after_prior_ops(monkeypatch, capsys):
    """
    TC-9.9: After a valid credit, an excessive debit is still rejected and balance unchanged.
    """
    data.write_balance(Decimal("40.00"))
    _set_input(monkeypatch, ["10.00"])
    operations.credit()
    _set_input(monkeypatch, ["100.00"])
    operations.debit()
    out = capsys.readouterr().out
    assert "Insufficient funds for this debit." in out
    assert data.read_balance() == Decimal("50.00")


def test_TC_9_10_large_credit_then_large_debit_to_penny(monkeypatch):
    """
    TC-9.10: Large credit then large debit leaves a minimal remaining balance.
    """
    data.write_balance(Decimal("0.00"))
    _set_input(monkeypatch, ["1000000.00"])
    operations.credit()
    _set_input(monkeypatch, ["999999.99"])
    operations.debit()
    assert data.read_balance() == Decimal("0.01")
