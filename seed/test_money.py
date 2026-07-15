"""The suite that ships with the repo."""

from money import round_cash


def test_already_a_nickel():
    assert round_cash(1000) == 1000


def test_small_remainder():
    # 1002¢: rounds to 1000 whether you go down or to nearest — direction doesn't show here.
    assert round_cash(1002) == 1000


def test_zero():
    assert round_cash(0) == 0
