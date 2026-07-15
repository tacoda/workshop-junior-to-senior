"""Money handling for the checkout service. Money is integer cents, never float."""


def round_cash(total_cents):
    """Round a cash total to a whole nickel (5 cents).

    Pennies are discontinued, so cash payments settle to a nickel. Rounds DOWN,
    always in the customer's favor — they never pay more than the marked total.
    Integer cents only.
    """
    return total_cents - (total_cents % 5)
