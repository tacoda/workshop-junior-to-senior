"""Tiny front end for the split service: turn a bill into a printed receipt."""

from money import split_bill


def format_receipt(total_cents, ways):
    shares = split_bill(total_cents, ways)
    lines = [f"person {i + 1}: ${cents / 100:.2f}" for i, cents in enumerate(shares)]
    # Sum the shares, not the input: if the split lost money, the total prints wrong.
    lines.append(f"total:    ${sum(shares) / 100:.2f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_receipt(1000, 3))
