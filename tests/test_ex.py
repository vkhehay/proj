# file name should be start with test_
import pytest


def add(a, b):
    return a + b


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise Exception("you have not enough money on balance")
        else:
            self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1


@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (12, 6, 18),
    (4, 9, 13)
])
def test_add(num1, num2, result):  # function name should be started with test_
    print('testing function')
    assert add(num1, num2) == result


@pytest.fixture
def zero_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(100)


def test_zero_account(zero_account):
    zero_account.deposit(50)
    assert zero_account.balance == 50


def test_bank_account_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 110


def test_bank_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 50


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 4) == 110


@pytest.mark.parametrize("deposited, withdrew, result", [
    (200, 100, 100),
    (150, 70, 80)
])
def test_bank_transaction(zero_account, deposited, withdrew, result):
    zero_account.deposit(deposited)
    zero_account.withdraw(withdrew)
    assert zero_account.balance == result


def test_insufficient_balance(bank_account):
    with pytest.raises(Exception):  # to catch raised Exceptions and pass the tests
        bank_account.withdraw(150)

# to run the test the command in the terminal is python -m pytest
# tests\test_ex.py .

# additional argument -v (Display pytest version and information about plugins.)
# tests/test_ex.py::test_add PASSED

# additional argument -s (Shortcut for --capture=no):
# tests/test_ex.py::test_add testing function
# PASSED

# with argument -s but without -v:
# tests\test_ex.py testing function
# .
# argument -x brake testing on first failed test
