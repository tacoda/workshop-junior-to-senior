"""Tiny front end for the checkout service: turn a bill into a printed receipt."""

from money import round_cash

BILL_CENTS = 1083  # $10.83


def format_receipt(total_cents):
    cash = round_cash(total_cents)
    return "\n".join([
        f"total:      ${total_cents / 100:.2f}",
        f"cash total: ${cash / 100:.2f}",   # rounded to a nickel — pennies are discontinued
    ])


if __name__ == "__main__":
    print(format_receipt(BILL_CENTS))
