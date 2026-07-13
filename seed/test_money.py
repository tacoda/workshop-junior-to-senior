"""The suite that ships with the repo.

Note for instructors: these tests only exercise divisible totals, so both the
correct split and the planted "simplification" pass them. That is deliberate —
green here means "the tests that exist passed," not "the code is correct." The
conservation gate learners write in Module 4 is what actually catches the plant.
"""

import pytest

from money import split_bill


def test_even_split():
    assert split_bill(1000, 4) == [250, 250, 250, 250]


def test_one_share_per_person():
    assert len(split_bill(1000, 3)) == 3


def test_rejects_zero_ways():
    with pytest.raises(ValueError):
        split_bill(1000, 0)
