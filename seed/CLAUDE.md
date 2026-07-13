# split — a bill-splitting service

A tiny service that splits a bill evenly across people. Small enough to hold in your head,
which is the point: you should be able to comprehend every line before you change it.

## Run it
    python app.py

## Test it
    pip install pytest && pytest

## Money
Money is handled as **integer cents** — see `money.py`. Formatting to dollars happens only at
the edge, when printing a receipt.

## Rules
> Module 2 artifact: you author the money rule here. A starting point:
>
> - **Iron law:** money is integer cents; never use float to store or compute money.
> - **Golden rule:** any function that splits or moves money must conserve the total, and
>   ship the conservation test that proves it.
> - **Preference:** format money for display only, never mid-calculation.
