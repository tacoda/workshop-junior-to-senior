"""Money handling for the split service. Money is integer cents, never float."""


def split_bill(total_cents, ways):
    """Split a bill evenly across `ways` people.

    Returns a list of `ways` integer-cent shares. The shares always sum back to
    `total_cents` — remainder cents are handed out one each to the first people,
    so no money is created or destroyed.
    """
    if ways <= 0:
        raise ValueError("ways must be positive")
    base, remainder = divmod(total_cents, ways)
    return [base + (1 if i < remainder else 0) for i in range(ways)]
