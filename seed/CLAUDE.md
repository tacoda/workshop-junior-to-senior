# checkout — a tiny cash-register service

A tiny service that settles a bill for cash and prints a receipt. Small enough to hold in your
head, which is the point: you should be able to comprehend every line before you change it.

## Run it
    python app.py

## Test it
    pip install pytest && pytest

## Money
Money is handled as **integer cents** — see `money.py`. Formatting to dollars happens only at the
edge, when printing a receipt.

## Rules
> Learners author these rules. The load-bearing one is the cash-rounding policy — a decision the
> code makes silently unless you make it explicit.
>
> - **Iron law:** money is integer cents; never use `float` to store or compute money.
> - **Rounding policy:** pennies are discontinued, so cash totals round to a nickel (5 cents).
>   Round **DOWN**, always in the **customer's favor** — never round up, and never round to the
>   nearest nickel. A customer never pays more than the marked total.
> - **Preference:** format money for display only, never mid-calculation.
